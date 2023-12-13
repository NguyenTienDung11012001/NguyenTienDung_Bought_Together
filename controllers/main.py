import werkzeug
from odoo import http
from odoo.http import request, route
import json
import shopify


class SampleApp(http.Controller):
    @route('/bought-together', auth='public', type='http')
    def bought_together(self, **kwargs):
        # Setup session
        api_key = 'c60b8fd403b8bccfe276c074d5c3ac7d'
        shared_secret = '40b06649b9edd378ff3b67ca0f836385'
        shopify.Session.setup(api_key=api_key, secret=shared_secret)

        # Create session
        shop_url = kwargs['shop']
        api_version = '2023-04'
        new_session = shopify.Session(shop_url, api_version)

        # Redirect to authenticate
        redirect_uri = "https://odoo.website/dashboard/store"
        scopes = ['read_products', 'read_orders']
        auth_url = new_session.create_permission_url(scopes, redirect_uri)

        return werkzeug.utils.redirect(auth_url)

    @http.route(['/dashboard/<string:name>',
                 '/dashboard/store/<string:name>'], auth='user', type='http')
    def dashboard_store(self):
        current_uid = request.env.context.get('uid')
        cur_user = request.env['res.users'].browse(current_uid)
        at_model = request.env['access.token'].search([])
        widget_model = request.env['bt.widget']

        stores = []
        for m in at_model:
            wgs = widget_model.sudo().search([('shop_id', '=', m.id)])
            included = 0
            for w in wgs:
                included += len(w.product_ids)
            stores.append({
                'key': m.shop_name,
                'name': m.shop_name,
                'included': included,
                'status': m.shop_status,
            })

        value = {
            'user_name': cur_user.name,
            'user_image': cur_user.image_1920.decode('utf-8'),
            'stores': stores,
        }

        return request.render('oath2_ex.sample_app_template', {'app_settings': json.dumps(value)})

    @http.route('/oath2-ex/get-store-data', type='json', auth='public')
    def get_store_data(self, name):
        data_recommend_table = self.get_widget_products(name, 'recommendation')
        data_excluded_table = self.get_widget_products(name, 'excluded')
        store_status = request.env['access.token'].sudo().search([('shop_name', '=', name)]).shop_status

        value = {
            'store': name,
            'store_status': store_status,
            'dataRecommendTable': data_recommend_table,
            'dataExcludedTable': data_excluded_table,
        }
        return value

    @staticmethod
    def get_widget_products(shop_name, type):
        data = []
        shop = request.env['access.token'].sudo().search([('shop_name', '=', shop_name)])
        if shop:
            widget = request.env['bt.widget'].search([('shop_id', '=', shop.id), ('type', '=', type)])
            if widget:
                for p in widget.product_ids:
                    data.append({
                        "key": p.product_id,
                        "title": p.name,
                        "url": p.url,
                        "price": p.price,
                        "compare": p.compare,
                        "quantity": p.compare,
                    })
        return data

    @http.route('/oath2-ex/search-product', type='json', auth='public')
    def search_product(self, keyword=None, shop=None):
        access_token = request.env['access.token'].search([('shop_name', '=', shop)]).access_token
        shop_url = f'{shop}.myshopify.com'
        api_version = '2023-04'
        session = shopify.Session(shop_url, api_version, access_token)
        shopify.ShopifyResource.activate_session(session)

        left_query = """
                        query {
                            productVariants(first: 5"""
        right_query = """) {
                                edges {
                                    node {
                                        id
                                        displayName
                                        product {
                                            title
                                            featuredImage {
                                                url  
                                            }
                                        }
                                        price
                                        compareAtPrice        
                                        inventoryQuantity                    
                                    }
                                } 
                            }
                        }
                    """

        if keyword:
            # execute a graphQL call
            mid_query = f', query: "title: {keyword}"'
            result = shopify.GraphQL().execute(left_query + mid_query + right_query)

            return json.loads(result)['data']['productVariants']['edges']
        else:
            result = shopify.GraphQL().execute(left_query + right_query)

            return json.loads(result)['data']['productVariants']['edges']

    @http.route('/oath2-ex/save-product', type='json', auth='public')
    def save_product(self, shop, data=None, type=None):
        shop_id = request.env['access.token'].search([('shop_name', '=', shop)]).id
        type = type
        shopify_product_model = request.env['shopify.product']
        bt_widget_model = request.env['bt.widget']

        product_ids = []
        for item in data:
            product = shopify_product_model.search([('product_id', '=', item.get('key')), ('shop_id', '=', shop_id)])
            if not product:
                product = shopify_product_model.sudo().create({
                    'name': item.get('title'),
                    'price': item.get('price'),
                    'product_id': item.get('key'),
                    'shop_id': shop_id,
                    'url': item.get('url'),
                    'compare': item.get('compare'),
                    'quantity': item.get('quantity'),
                })
            product_ids.append(product.id)

        widget_data = bt_widget_model.search([('shop_id', '=', shop_id), ('type', '=', type)])
        if not widget_data:
            bt_widget_model.sudo().create({
                'shop_id': shop_id,
                'product_ids': product_ids,
                'type': type,
            })
        else:
            if product_ids == []:
                widget_data.sudo().write({
                    'product_ids': [(5, 0)],
                })
            else:
                widget_data.sudo().write({
                    'product_ids': product_ids,
                })

        return "{'status': 'Ok'}"

    @http.route('/oath2-ex/change-store-status', type='json', auth='public')
    def change_store_status(self, store, status):
        shop = request.env['access.token'].search([('shop_name', '=', store)])
        if shop:
            shop.shop_status = status

    @route('/oath2-ex/get-customization', type='json', auth='public')
    def get_customization(self, shop):
        shop = request.env['access.token'].search([('shop_name', '=', shop)])
        if shop:
            print(shop.customization_setting)
            return shop.customization_setting

    @route('/oath2-ex/save-customization', type='json', auth='public')
    def save_customization(self, shop, data):
        shop = request.env['access.token'].search([('shop_name', '=', shop)])
        if shop:
            shop.sudo().write({
                'customization_setting': data,
            })
