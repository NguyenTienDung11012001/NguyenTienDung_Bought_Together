from odoo import fields, models, api


class ShopifyOrder(models.Model):
    _name = 'shopify.order'
    _description = 'shopify order'

    order_id = fields.Char('Shopify order id')
    shop_id = fields.Many2one('access.token', string='Shop URL')
    name = fields.Char('order name')
    contact = fields.Many2one('shopify.contact', string='Contact')
    order_line_ids = fields.One2many('shopify.order.line', 'order_id', string='Order line')
    xero_invoice_id = fields.Char('Xero Invoice ID')
    financial_status = fields.Char('Order Status')
    date = fields.Date('Order Date')
