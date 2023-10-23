from odoo import fields, models, api


class ShopifyOrder(models.Model):
    _name = 'shopify.order'

    order_id = fields.Char('shopify order id')
    name = fields.Char('order name')
    contact = fields.Char('contact email')
    total_price = fields.Char('total price')
    shop_url_id = fields.Many2one('access.token', string='Shop URL')