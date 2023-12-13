from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'bt.widget'
    _description = 'Product of Bought Together'

    shop_id = fields.Char('Shop')
    product_ids = fields.Many2many('shopify.product', string='Product in widget')
    type = fields.Char('Type')
