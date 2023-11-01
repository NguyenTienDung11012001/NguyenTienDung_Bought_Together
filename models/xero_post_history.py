from odoo import fields, models, api
import datetime


class XeroPostHistory(models.Model):
    _name = 'xero.post.history'
    _description = 'History post invoices and payments to Xero'

    date = fields.Date(string='Date', default=datetime.datetime.now())
    shopify_id = fields.Many2one('access.token', string='Shopify Shop')
    total_invoices = fields.Integer('Total Invoices')
    total_payments = fields.Integer('Total Payments')
