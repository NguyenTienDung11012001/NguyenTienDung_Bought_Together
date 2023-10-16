from odoo import http
import werkzeug
import shopify
import traceback


class ShopifyAPI(http.Controller):
    @http.route('/test-shopify', auth='public', type='http')
    def test_shopify(self):
        api_key = 'c755092526e32bb09b8c9afa8b1b34d6'
        shared_secred = 'fdb10b3c36c7d01e488c590bf8296e08'

        shopify.Session.setup(api_key=api_key, secret=shared_secred)

        shop_url = "dungtien111.myshopify.com"
        api_version = '2023-04'
        redirect_uri = "https://odoo.website/test-shopify/finalize"
        scopes = ['read_products', 'read_orders']

        new_session = shopify.Session(shop_url, api_version)

        auth_url = new_session.create_permission_url(scopes, redirect_uri)

        return werkzeug.utils.redirect(auth_url)

    @http.route('/test-shopify/finalize', auth='public', type='http')
    def test_shopify_finalize(self, **kwargs):
        try:
            api_key = 'c755092526e32bb09b8c9afa8b1b34d6'
            shared_secred = 'fdb10b3c36c7d01e488c590bf8296e08'

            shopify.Session.setup(api_key=api_key, secret=shared_secred)

            api_version = '2023-04'
            shop_url = kwargs['shop']

            session = shopify.Session(shop_url, api_version)

            access_token = session.request_token(kwargs)

            session = shopify.Session(shop_url, api_version, access_token)
            shopify.ShopifyResource.activate_session(session)
            # shop = shopify.Shop.current()  # Get the current shop
            # products = shopify.Product.find()  # Get a specific product

            model = http.request.env['access.token']
            val = model.sudo().search([('shopName', '=', shop_url)])

            if not val:
                model.sudo().create({'shopName': shop_url, 'token': access_token})
            else:
                val.sudo().write({'token': access_token})

            return '123'
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            return 'Error'
