from odoo import http
from odoo.http import route, request


class OrderController(http.Controller):

    @route('/test-shopify/<string:shop_url>/orders/create', auth='public', type='json')
    def test_shopify_create_orders(self, shop_url):
        val = request.jsonrequest
        model = request.env['shopify.order']
        shop = request.env['access.token'].search([('shop_url', '=', shop_url)])
        print(val)
        print(model)
        print(shop)
        model.sudo().create({
            'order_id': val.get('id'),
            'name': val.get('name'),
            'contact': val.get('contact_email'),
            'total_price': val.get('current_total_price'),
            'shop_url_id': shop.id
        })

        return '{"response": "OK"}'

    @route('/test-shopify/<string:shop_url>/orders/updated', auth='public', type='json')
    def test_shopify_update_orders(self, shop_url):
        val = request.jsonrequest
        shop = request.env['access.token'].search([('shop_url', '=', shop_url)])
        order = request.env['shopify.order'].search([('order_id', '=', val['id']), ('shop_url_id', '=', shop.id)])
        if order:
            order.sudo().write({
                'name': val.get('name'),
                'contact': val.get('contact_email'),
                'total_price': val.get('current_total_price'),
            })

        return '{"response": "OK"}'

    @route('/test-shopify/<string:shop_url>/orders/cancelled', auth='public', type='json')
    def test_shopify_delete_orders(self, shop_url):
        val = request.jsonrequest
        shop = request.env['access.token'].search([('shop_url', '=', shop_url)])
        order = request.env['shopify.order'].search([('order_id', '=', val['id']), ('shop_url_id', '=', shop.id)])
        if order:
            order.sudo().unlink()

        return '{"response": "OK"}'
