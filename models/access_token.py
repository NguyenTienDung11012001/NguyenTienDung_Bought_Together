from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'access.token'
    _description = 'Access token shopify shop'

    shopName = fields.Char('Shop name', required=True)
    token = fields.Char('Token', required=True)
