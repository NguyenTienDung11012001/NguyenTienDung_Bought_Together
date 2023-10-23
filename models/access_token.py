import werkzeug
from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'access.token'
    _description = 'Access token shopify shop'

    shop_name = fields.Char('Name', compute='_compute_name_shop')
    shop_url = fields.Char('Shop_url')
    access_token = fields.Char('Access Token')
    currency = fields.Char('Currency')
    country_name = fields.Char('Country')
    email = fields.Char('Email')

    @api.depends('shop_url')
    def _compute_name_shop(self):
        for line in self:
            line.shop_name = line.shop_url.split(".myshopify.com")[0]

    def redirect_home_app(self):
        url = f'https://admin.shopify.com/store/{self.shop_url.split(".")[0]}'
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url
        }

    def name_get(self):
        res = []
        for record in self:
            name = record.shop_name
            res.append((record.id, name))
        return res

