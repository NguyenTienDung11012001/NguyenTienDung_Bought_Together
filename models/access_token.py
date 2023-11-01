import werkzeug
from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'access.token'
    _description = 'Access token to shopify shop'

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

    def view_products(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'res_model': 'shopify.product',
            'domain': [('shop_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
            'help': '''
                <p class="o_view_nocontent_smiling_face">
                    There is no examples click here to add new Order.
                </p>
            '''
        }

    def view_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'res_model': 'shopify.order',
            'domain': [('shop_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
            'help': '''
                <p class="o_view_nocontent_smiling_face">
                    There is no examples click here to add new Order.
                </p>
            '''
        }

    def name_get(self):
        res = []
        for record in self:
            name = record.shop_name
            res.append((record.id, name))
        return res

    def connect_xero(self):
        client_id = 'C1057113036B42BB827382B4BB0F24DF'
        state = self.id
        url = f'https://login.xero.com/identity/connect/authorize?response_type=code&client_id={client_id}&redirect_uri=https%3A%2F%2Fodoo.website%2Ftest-xero%2Ffinalize&scope=openid profile email accounting.transactions accounting.contacts accounting.settings offline_access&state={state}'
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    def view_xero(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Xero Token',
            'res_model': 'xero.token',
            'domain': [('shopify_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
            'help': '''Click connect to get xero access token'''
        }


