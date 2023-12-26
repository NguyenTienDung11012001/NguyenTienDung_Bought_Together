from odoo import fields, models, api


class ShopifyOrderLine(models.Model):
    _name = 'shopify.order.line'
    _description = 'Shopify Order Line'

    order_id = fields.Many2one('shopify.order', string='Order ID')
    product_id = fields.Many2one('shopify.product', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', default='1')
    unit_amount = fields.Float(string='Unit Amount', related='product_id.price', store=True)
    account_code = fields.Char(string='Account Code', default='200')
    line_amount = fields.Integer(string='Line Amount', compute='_compute_amount', store=True)
    line_item_id = fields.Char(string='Line Item ID')

    @api.depends('quantity', 'unit_amount')
    def _compute_amount(self):
        for line in self:
            line.line_amount = line.unit_amount * line.quantity
