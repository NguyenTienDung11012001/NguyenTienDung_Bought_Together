from odoo import http
from odoo.http import route, request


class ProductController(http.Controller):

    @route('/test-shopify/<string:shop_url>/products/create', auth='public', type='json')
    def test_shopify_create(self, shop_url):
        val = request.jsonrequest
        model = request.env['shopify.product']
        shop = request.env['access.token'].search([('shop_url', '=', shop_url)])
        model.sudo().create({
            'product_id': val.get('id'),
            'title': val.get('title'),
            'body_html': val.get('body_html'),
            'vendor': val.get('vendor'),
            'product_type': val.get('product_type'),
            'status': val.get('status'),
            'shop_url_id': shop.id
        })

        return '{"response": "OK"}'

    @route('/test-shopify/<string:shop_url>/products/update', auth='public', type='json')
    def test_shopify_update(self, shop_url):
        val = request.jsonrequest
        shop = request.env['access.token'].search([('shop_url', '=', shop_url)])
        product = request.env['shopify.product'].search([('product_id', '=', val['id']), ('shop_url_id', '=', shop.id)])
        if product:
            product.sudo().write({
                'title': val.get('title'),
                'body_html': val.get('body_html'),
                'vendor': val.get('vendor'),
                'product_type': val.get('product_type'),
                'status': val.get('status'),
            })

        return '{"response": "OK"}'

    @route('/test-shopify/<string:shop_url>/products/delete', auth='public', type='json')
    def test_shopify_delete(self, shop_url):
        val = request.jsonrequest
        shop = request.env['access.token'].search([('shop_url', '=', shop_url)])
        product = request.env['shopify.product'].search([('product_id', '=', val['id']), ('shop_url_id', '=', shop.id)])
        if product:
            product.sudo().unlink()

        return '{"response": "OK"}'
