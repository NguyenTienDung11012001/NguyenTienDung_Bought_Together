from odoo import http
from odoo.http import route, request
import shopify, binascii, os


class OdooHospital(http.Controller):
    @http.route('/test', auth='public', type='http', website=True)
    def display_register(self, **kw):
        partner = request.env['res.partner'].search([])
        vals = {
            'page_name': 'test_controller',
            'partner': partner
        }
        if request.httprequest.method == "POST":
            # request.env['hospital.patient'].create({'name': kw['name'],
            #                                         'age': kw['age'],
            #                                         'gender': kw['gender'],
            #                                         'responsible_id': kw['responsible_id'],
            #                                         'note': kw['note']})
            print(kw)

        return request.render('test_controller.test_template', vals)

    @http.route('/test/receive', auth='public', type='http', website=True)
    def create(self, **kw):
        print('efafsdf  ')
        return 'hello'

    # @http.route('/test-shopify', auth='public', type='http')
    # def test_shopify(self, **kw):
    #     return
    # API_KEY = '3d84fd2ce5d1ef0e2d9af4868ba744a0'
    # API_SECRET = '0e957ada79d4cd291f67715500bac3b2'
    #
    # shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)
    #
    # shop_url = "dungtien111.myshopify.com"
    # api_version = '2020-10'
    # state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    # redirect_uri = "http://myapp.com/auth/shopify/callback"
    # scopes = ['read_products', 'read_orders']
    #
    # newSession = shopify.Session(shop_url, api_version)
    # auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
    # # redirect to auth_url
    #
    # session = shopify.Session(shop_url, api_version)
    # access_token = session.request_token(request_params)  # request_token will validate hmac and timing attacks
    # # you should save the access token now for future use.
    #
    # session = shopify.Session(shop_url, api_version, access_token)
    # shopify.ShopifyResource.activate_session(session)
    #
    # shop = shopify.Shop.current()  # Get the current shop
    # product = shopify.Product.find(179761209)  # Get a specific product
    #
    # # execute a graphQL call
    # shopify.GraphQL().execute("{ shop { name id } }")
    #
    # shopify.ShopifyResource.clear_session()
