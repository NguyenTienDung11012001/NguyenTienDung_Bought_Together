from odoo import fields, models, api
import datetime
import base64
import requests
from odoo.exceptions import ValidationError


class ModelName(models.Model):
    _name = 'xero.token'
    _description = 'Xero access token'

    access_token = fields.Char('Access Token')
    refresh_token = fields.Char('Refresh Token')
    access_token_time_out = fields.Datetime('Access Token Time Out')
    refresh_token_time_out = fields.Datetime('Refresh Token Time Out')
    shopify_id = fields.Many2one('access.token', string='Shopify shop ID')
    state = fields.Selection([('disconnected', 'Disconnected'), ('connected', 'Connected')], default='disconnected',
                             string='Status', compute='_compute_state')
    tenant_id = fields.Char('Tenant ID')

    @api.depends('access_token_time_out')
    def _compute_state(self):
        for line in self:
            if line.access_token_time_out > datetime.datetime.now():
                line.state = 'connected'
            else:
                line.state = 'disconnected'

    def reconnect_xero(self):
        if self.refresh_token_time_out > datetime.datetime.now():
            client_id = self.env['ir.config_parameter'].sudo().get_param('oath2_ex.xero_client_id')
            client_secret = self.env['ir.config_parameter'].sudo().get_param('oath2_ex.xero_client_secret')
            credentials = f"{client_id}:{client_secret}"
            base64_credentials = base64.b64encode(credentials.encode()).decode()

            headers = {
                'authorization': f'Basic {base64_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            data = {
                'grant_type': 'refresh_token',
                'refresh_token': f'{self.refresh_token}'
            }

            response = requests.post(url='https://identity.xero.com/connect/token', data=data, headers=headers)
            time_now = datetime.datetime.now()

            if response.status_code == 200:
                self.access_token = response.json()['access_token']
                self.refresh_token = response.json()['refresh_token']
                self.access_token_time_out = time_now + datetime.timedelta(minutes=30)
                self.refresh_token_time_out = time_now + datetime.timedelta(days=60)
            else:
                raise ValidationError("Cannot reconnect to Xero")
        else:
            raise ValidationError("Refresh Token out of time")

    def post_invoices(self):
        if self.state == 'connected':
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Xero-Tenant-Id': self.tenant_id,
                'Content-Type': 'application/json',
                "Accept": "application/json"
            }

            total_invoices = 0
            total_payments = 0

            # post invoices
            invoices = []
            orders = self.env['shopify.order'].search([('shop_id', '=', self.shopify_id.id),
                                                       ('xero_invoice_id', '=', None)])
            for order in orders:
                # create xero contact
                contact = self.env['shopify.contact'].search([('id', '=', order.contact.id)])
                if not contact.xero_contact_id:
                    json = {
                        'Contacts': [
                            {
                                'name': contact.name
                            }
                        ]
                    }
                    response = requests.post(url='https://api.xero.com/api.xro/2.0/Contacts', headers=headers,
                                             json=json)
                    contact_id = response.json()["Contacts"][0]["ContactID"]
                    contact.write({
                        'xero_contact_id': contact_id
                    })
                else:
                    contact_id = contact.xero_contact_id

                # create invoice line
                lineItems = []
                order_lines = self.env['shopify.order.line'].search([('order_id', '=', order.id)])
                for order_line in order_lines:
                    lineItems.append({
                        "Description": order_line.product_id.name,
                        "Quantity": order_line.quantity,
                        "UnitAmount": order_line.unit_amount,
                        "AccountCode": "200",
                        "LineAmount": order_line.line_amount
                    })

                # create invoice
                invoice = {
                    "Type": "ACCREC",
                    "Contact": {
                        "ContactID": contact_id
                    },
                    "LineItems": lineItems,
                    "Status": 'AUTHORISED',
                    "DueDate": "2024-12-12",
                    "Reference": order.order_id
                }
                invoices.append(invoice)
                total_invoices += 1

            if invoices:
                json = {
                    "Invoices": invoices
                }

                # post invoices
                response = requests.post(url='https://api.xero.com/api.xro/2.0/Invoices', headers=headers,
                                         json=json).json()

                # save invoice id
                if response['Status'] and response['Status'] == 'OK':
                    for invoice in response['Invoices']:
                        model = self.env['shopify.order'].search([('shop_id', '=', self.shopify_id.id),
                                                                  ('order_id', '=', invoice['Reference'])])
                        model.write({
                            'xero_invoice_id': invoice['InvoiceID']
                        })

                    # change invoices to payments
                    payments = []
                    invoices_paid = self.env['shopify.order'].search([('shop_id', '=', self.shopify_id.id),
                                                                      ('xero_invoice_id', '!=', None),
                                                                      ('financial_status', '=', 'paid')])
                    for invoice_paid in invoices_paid:
                        # create payment invoice line items
                        invoice_lines = self.env['shopify.order.line'].search([('order_id', '=', invoice_paid.id)])
                        line_items = []
                        payment_amount = 0
                        for invoice_line in invoice_lines:
                            line_items.append({
                                "Description": invoice_line.product_id.name,
                                "Quantity": invoice_line.quantity,
                                "UnitAmount": invoice_line.unit_amount,
                                "AccountCode": "200",
                                "LineAmount": invoice_line.line_amount
                            })
                            payment_amount += invoice_line.line_amount

                        # create payment
                        payments.append({
                            "Invoice": {
                                "LineItems": line_items,
                                "InvoiceID": invoice_paid.xero_invoice_id
                            },
                            "Account": {
                                "Code": "970"
                            },
                            "Date": "2024-12-12",
                            "Amount": payment_amount
                        })
                        total_payments += 1

                    payments_json = {
                        'Payments': payments
                    }
                    # post payments
                    payment_response = requests.post(url='https://api.xero.com/api.xro/2.0/Payments', headers=headers,
                                                     json=payments_json)
                    print(payment_response.status_code)
                    print(payment_response.json())

                    # log history
                    self.env['xero.post.history'].create({
                        'shopify_id': self.shopify_id.id,
                        'total_invoices': total_invoices,
                        'total_payments': total_payments,
                    })

                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'message': f'Post {total_invoices} invoices and create {total_payments} payments',
                            'type': 'success',
                            'sticky': False,
                        },
                    }
            else:
                raise ValidationError("Nothing to post!")
        else:
            raise ValidationError("Connect to Xero first")
