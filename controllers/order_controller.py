from odoo import http
from odoo.http import route, request


class OrderController(http.Controller):

    @route('/test-shopify/<string:shop_url>/orders/create', auth='public', type='json')
    def test_shopify_create_orders(self, shop_url):
        val = request.jsonrequest
        contact_model = request.env['shopify.contact']
        order_model = request.env['shopify.order']
        product_model = request.env['shopify.product']
        shop_model = request.env['access.token'].search([('shop_url', '=', shop_url)])
        order_line_model = request.env['shopify.order.line']

        order_line_ids = []
        for line_item in val.get('line_items'):
            product = product_model.search([('product_id', '=', line_item.get('product_id')),
                                            ('shop_id', '=', shop_model.id)])
            if not product:
                product = product_model.sudo().create({
                    'product_id': line_item.get('product_id'),
                    'name': line_item.get('name'),
                    'price': line_item.get('price'),
                    'shop_id': shop_model.id
                })

            order_line = order_line_model.create({
                'product_id': product.id,
                'quantity': line_item.get('quantity'),
                'unit_amount': product.price,
                'line_item_id': line_item.get('id')
            })
            order_line_ids.append(order_line.id)
        print('order_line_ids: ', order_line_ids)
        #
        contact = contact_model.search([('shopify_contact_id', '=', val.get('customer').get('id')),
                                        ('shop_id', '=', shop_model.id)])
        if not contact:
            contact = contact_model.create({
                'shopify_contact_id': val.get('customer').get('id'),
                'name': f"{val.get('customer').get('first_name')} {val.get('customer').get('last_name')}",
                'phone': val.get('customer').get('email'),
                'email': val.get('customer').get('phone'),
                'shop_id': shop_model.id
            })
        print('contact: ', contact)

        if order_line_ids and contact:
            order = order_model.sudo().create({
                'order_id': val.get('id'),
                'shop_id': shop_model.id,
                'name': val.get('name'),
                'contact': contact.id,
                'order_line_ids': order_line_ids,
                'financial_status': val.get('financial_status'),
                'date': val.get('updated_at')
            })
            print('order: ', order)

        return '{"response": "OK"}'

    @route('/test-shopify/<string:shop_url>/orders/updated', auth='public', type='json')
    def test_shopify_update_orders(self, shop_url):
        val = request.jsonrequest
        product_model = request.env['shopify.product']
        order_line_model = request.env['shopify.order.line']
        shop_model = request.env['access.token'].search([('shop_url', '=', shop_url)])
        order = request.env['shopify.order'].search([('order_id', '=', val.get('id')), ('shop_id', '=', shop_model.id)])

        if order and val.get('line_items'):
            order_line_ids = []
            for line_item in val.get('line_items'):
                order_line = order_line_model.search([('line_item_id', '=', line_item.get('id'))])
                if order_line:
                    order_line.write({
                        'quantity': line_item.get('quantity'),
                    })
                else:
                    product = product_model.search([('product_id', '=', line_item.get('product_id')),
                                                    ('shop_id', '=', shop_model.id)])
                    if not product:
                        product = product_model.sudo().create({
                            'product_id': line_item.get('product_id'),
                            'name': line_item.get('name'),
                            'price': line_item.get('price'),
                            'shop_id': shop_model.id
                        })
                    order_line = order_line_model.create({
                        'product_id': product.id,
                        'quantity': line_item.get('quantity'),
                        'unit_amount': product.price,
                        'line_item_id': line_item.get('id')
                    })
                order_line_ids.append(order_line.id)

            order.sudo().write({
                'name': val.get('name'),
                'order_line_ids': order_line_ids,
                'financial_status': val.get('financial_status'),
                'date': val.get('updated_at'),
            })

        return '{"response": "OK"}'

    @route('/test-shopify/<string:shop_url>/orders/cancelled', auth='public', type='json')
    def test_shopify_delete_orders(self, shop_url):
        val = request.jsonrequest
        shop = request.env['access.token'].search([('shop_url', '=', shop_url)])
        order = request.env['shopify.order'].search([('order_id', '=', val['id']), ('shop_id', '=', shop.id)])
        if order:
            order.sudo().unlink()

        return '{"response": "OK"}'
