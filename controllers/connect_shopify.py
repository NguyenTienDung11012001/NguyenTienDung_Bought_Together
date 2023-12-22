from odoo import http
import werkzeug
import shopify
import traceback
from odoo.http import route, request


class ShopifyAPI(http.Controller):
    @route('/test-shopify', auth='public', type='http')
    def test_shopify(self, **kwargs):
        # Setup session
        api_key = request.env['ir.config_parameter'].sudo().get_param('oath2_ex.shopify_api_key')
        shared_secret = request.env['ir.config_parameter'].sudo().get_param('oath2_ex.shopify_secret_key')
        shopify.Session.setup(api_key=api_key, secret=shared_secret)

        # Create session
        shop_url = kwargs['shop']
        api_version = request.env['ir.config_parameter'].sudo().get_param('oath2_ex.shopify_api_version')
        new_session = shopify.Session(shop_url, api_version)

        # Redirect to authenticate
        redirect_uri = "https://odoo.website/test-shopify/finalize"
        scopes = ['read_products', 'read_orders']
        auth_url = new_session.create_permission_url(scopes, redirect_uri)

        return werkzeug.utils.redirect(auth_url)

    @route('/test-shopify/finalize', auth='public', type='http')
    def test_shopify_finalize(self, **kwargs):
        try:
            # Setup session
            api_key = request.env['ir.config_parameter'].sudo().get_param('oath2_ex.shopify_api_key')
            shared_secret = request.env['ir.config_parameter'].sudo().get_param('oath2_ex.shopify_secret_key')
            shopify.Session.setup(api_key=api_key, secret=shared_secret)

            # Create session
            shop_url = kwargs['shop']
            api_version = request.env['ir.config_parameter'].sudo().get_param('oath2_ex.shopify_api_version')
            session = shopify.Session(shop_url, api_version)

            # get access token
            access_token = session.request_token(kwargs)

            # Activate session
            session = shopify.Session(shop_url, api_version, access_token)
            shopify.ShopifyResource.activate_session(session)

            # Manage Webhook
            address = request.env['ir.config_parameter'].sudo().get_param('oath2_ex.shopify_webhook_base_url')
            webhook = shopify.Webhook.find()

            # Destroy webhook because address changed
            for w in webhook:
                if not w.address.split('/test-shopify')[0] == address:
                    shopify.Webhook.destroy(w)

            topic = 'products'
            events = ['create', 'update', 'delete']
            self.create_webhook(self, address, shop_url, topic, events)

            topic = 'orders'
            events = ['create', 'updated', 'cancelled']
            self.create_webhook(self, address, shop_url, topic, events)

            # Save access token to db and redirect to form view
            model = request.env['access.token']
            val = model.sudo().search([('shop_url', '=', shop_url)])

            if not val:
                shop = shopify.Shop.current()
                data = model.sudo().create({
                    'shop_url': shop.myshopify_domain,
                    'access_token': access_token,
                    'currency': shop.currency,
                    'country_name': shop.country_name,
                    'email': shop.email
                })
                at_id = data.id
            else:
                at_id = val.id
                val.sudo().write({
                    'access_token': access_token
                })

            return request.redirect('/')
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            return 'Error'

    @staticmethod
    def create_webhook(self, address, shop_url, topic, events):
        for e in events:
            hook = self.get_hook(address, shop_url, topic, e)
            shopify.Webhook.create(hook)

    @staticmethod
    def get_hook(address, shop_url, topic, method):
        return {
            'topic': f'{topic}/{method}',
            'address': f'{address}/test-shopify/{shop_url}/{topic}/{method}',
            'format': 'json'
        }


