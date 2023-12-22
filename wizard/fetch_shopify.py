from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime
import shopify


class FetchShopify(models.TransientModel):
    _name = 'fetch.shopify.wizard'
    _description = 'fetch data from shopify'

    data = fields.Selection([('products', 'Products'),
                             ('orders', 'Orders')], string='Fetch data')
    shop_id = fields.Many2one('access.token', string='Shop')
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError("Start date cannot bigger than end date!")

    def fetch_shopify(self):
        # Activate session
        api_version = '2023-04'
        session = shopify.Session(self.shop_id.shop_url, api_version, self.shop_id.access_token)
        shopify.ShopifyResource.activate_session(session)
        count = 0

        # đoạn lây date_from và date_to phải truyền cả giờ vào, nếu không Shopify sẽ mặc định lấy 0h sáng làm mốc, do vậy có thể không fetch được order trong date_to
        date_from = self.date_from
        date_to = self.date_to
        datetime_from = datetime(date_from.year, date_from.month, date_from.day).replace(hour=0, minute=0,
                                                                                         second=0).strftime(
            "%Y-%m-%d %H:%M:%S")
        datetime_to = datetime(date_to.year, date_to.month, date_to.day).replace(hour=23, minute=59,
                                                                                 second=59).strftime(
            "%Y-%m-%d %H:%M:%S")
        type = ''

        # fetch product
        if self.data == 'products':
            type = 'products'
            shopify_products = shopify.Product.find(created_at_min=datetime_from, created_at_max=datetime_to)
            model = self.env['shopify.product']
            for p in shopify_products:
                try:
                    if not model.search([('product_id', '=', p.id), ('shop_id', '=', self.shop_id.id)]):
                        model.sudo().create({
                            'product_id': p.id,
                            'name': p.title,
                            'price': p.variants[0].price,
                            'shop_id': self.shop_id.id
                        })
                        count += 1
                except Exception as e:
                    continue

        # fetch order
        if self.data == 'orders':
            type = 'orders'
            shopify_orders = shopify.Order.find(created_at_min=datetime_from, created_at_max=datetime_to, status='any')
            order_model = self.env['shopify.order']
            order_line_model = self.env['shopify.order.line']
            contact_model = self.env['shopify.contact']
            product_model = self.env['shopify.product']

            for o in shopify_orders:
                try:
                    if not order_model.search([('order_id', '=', o.id), ('shop_id', '=', self.shop_id.id)]):
                        if o.customer is not None and o.line_items is not None:
                            # create order lines
                            order_line_ids = []
                            for item in o.line_items:
                                # fetch product
                                product = product_model.search([('product_id', '=', item.product_id),
                                                                ('shop_id', '=', self.shop_id.id)])
                                if not product:
                                    product = product_model.sudo().create({
                                        'product_id': item.product_id,
                                        'name': item.title,
                                        'price': item.price,
                                        'shop_id': self.shop_id.id
                                    })
                                # Create order line
                                order_line = order_line_model.create({
                                    'product_id': product.id,
                                    'quantity': item.quantity,
                                    'unit_amount': product.price,
                                    'line_item_id': item.id,
                                })
                                order_line_ids.append(order_line.id)

                            # fetch contact
                            contact = contact_model.search([('shopify_contact_id', '=', o.customer.id),
                                                            ('shop_id', '=', self.shop_id.id)])
                            if not contact:
                                contact = contact_model.create({
                                    'shopify_contact_id': o.customer.id,
                                    'name': f'{o.customer.first_name} {o.customer.last_name}',
                                    'phone': o.customer.email,
                                    'email': o.customer.phone,
                                    'shop_id': self.shop_id.id
                                })

                            # fetch order
                            order_model.sudo().create({
                                'order_id': o.id,
                                'shop_id': self.shop_id.id,
                                'name': o.name,
                                'contact': contact.id,
                                'order_line_ids': order_line_ids,
                                'financial_status': o.financial_status,
                                'date': o.updated_at
                            })
                            count += 1
                except Exception as e:
                    continue

        # log fetch history
        if count:
            self.env['fetch.history'].create({
                'data': type,
                'shop': self.shop_id.shop_name,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'count': count
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': f'fetch success {count} item',
                'type': 'success',
                'sticky': False,
            }
        }
