from odoo import fields, models, api


class ShopifyProduct(models.Model):
    _name = 'shopify.product'

    product_id = fields.Char('shopify product id')
    title = fields.Char('title')
    body_html = fields.Char('body_html')
    vendor = fields.Char('vendor')
    product_type = fields.Char('product_type')
    status = fields.Char('status')
    shop_url_id = fields.Many2one('access.token', string='Shop URL')
