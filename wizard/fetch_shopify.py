from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime
import shopify


class FetchShopify(models.TransientModel):
    _name = 'fetch.shopify.wizard'

    data = fields.Selection([('products', 'Products'),
                             ('orders', 'Orders')], string='Fetch data')
    shop_url = fields.Many2one('access.token', string='Shop')
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError("Start date cannot bigger than end date!")

    def fetch_shopify(self):
        # Setup session
        api_key = 'c755092526e32bb09b8c9afa8b1b34d6'
        shared_secret = 'fdb10b3c36c7d01e488c590bf8296e08'
        shopify.Session.setup(api_key=api_key, secret=shared_secret)

        # Activate session
        api_version = '2023-04'
        shop_url = self.shop_url.shop_url
        access_token = self.shop_url.access_token
        session = shopify.Session(shop_url, api_version, access_token)
        shopify.ShopifyResource.activate_session(session)

        count = 0
        # fetch product
        if self.data == 'products':
            shopify_products = shopify.Product.find()
            model = self.env['shopify.product']
            for p in shopify_products:
                product_date = datetime.strptime(p.updated_at.split("T")[0], '%Y-%m-%d').date()
                if self.date_from < product_date < self.date_to:
                    if not model.search([('product_id', '=', p.id), ('shop_url_id.shop_url', '=', shop_url)]):
                        model.sudo().create({
                            'product_id': p.id,
                            'title': p.title,
                            'body_html': p.body_html,
                            'vendor': p.vendor,
                            'product_type': p.product_type,
                            'status': p.status,
                            'shop_url_id': self.shop_url.id
                        })
                        count += 1

        # fetch order
        if self.data == 'orders':
            shopify_orders = shopify.Order.find()
            model = self.env['shopify.order']
            for o in shopify_orders:
                order_date = datetime.strptime(o.updated_at.split("T")[0], '%Y-%m-%d').date()
                if self.date_from < order_date < self.date_to:
                    if not model.search([('order_id', '=', o.id), ('shop_url_id.shop_url', '=', shop_url)]):
                        model.sudo().create({
                            'order_id': o.id,
                            'name': o.name,
                            'contact': o.contact_email,
                            'total_price': o.current_total_price,
                            'shop_url_id': self.shop_url.id
                        })
                        count += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': f'fetch success {count} item',
                'type': 'success',
                'sticky': False,
            }
        }
