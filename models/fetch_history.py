from odoo import fields, models, api


class FetchHistory(models.Model):
    _name = 'fetch.history'
    _description = 'fetch shopify data history'

    data = fields.Char()
    shop = fields.Char()
    date_from = fields.Char()
    date_to = fields.Char()
    count = fields.Integer()
