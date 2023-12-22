from odoo import fields, models, api


class ShopifyProduct(models.Model):
    _name = 'shopify.product'
    _description = 'shopify products'

    name = fields.Char('Name')
    price = fields.Float('Price')
    product_id = fields.Char('Shopify product id')
    shop_id = fields.Many2one('access.token', string='Shop')
    url = fields.Char('Image Url')
    compare = fields.Float('Compare')
    quantity = fields.Integer('Quantity')
