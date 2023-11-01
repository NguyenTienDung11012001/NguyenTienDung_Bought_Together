import base64

from odoo import http
from odoo.http import route, request
import requests
import werkzeug
import datetime
import json


class XeroAPI(http.Controller):

    @route('/test-xero/finalize', type="http", auth="public", website=True)
    def test_xero(self, **kwargs):
        # Define your client_id and client_secret
        client_id = 'C1057113036B42BB827382B4BB0F24DF'
        client_secret = 'IVoMSF2QnPfdeWhImsIsUkZadkA1xrMZnLanDdoFB_ARNNJ9'

        # Base64 encode client_id and client_secret for the Authorization header
        credentials = f"{client_id}:{client_secret}"
        base64_credentials = base64.b64encode(credentials.encode()).decode()

        # Get access token
        headers = {
            'authorization': f'Basic {base64_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'authorization_code',
            'code': kwargs['code'],  # Replace with your authorization code
            'redirect_uri': 'https://odoo.website/test-xero/finalize'  # Replace with your redirect URI
        }

        response = requests.post(url='https://identity.xero.com/connect/token', data=data, headers=headers)
        access_token = response.json()['access_token']

        # Get tenant_Id
        tenant_headers = {
            'authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        tenant_response = requests.get(url='https://api.xero.com/connections', headers=tenant_headers)
        tenant_id = tenant_response.json()[0]['tenantId']
        print(tenant_response.json())

        xero_token = request.env["xero.token"].search([('shopify_id', '=', kwargs['state'])])
        time_now = datetime.datetime.now()

        if xero_token:
            xero_token.write({
                'access_token': access_token,
                'refresh_token': response.json()['refresh_token'],
                'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                'tenant_id': tenant_id
            })
        else:
            request.env['xero.token'].create({
                'access_token': access_token,
                'refresh_token': response.json()['refresh_token'],
                'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                'shopify_id': kwargs['state'],
                'tenant_id': tenant_id
            })

        # # Get invoices
        # headers = {
        #     'authorization': f'Bearer {access_token}',
        #     'Content-Type': 'application/json',
        #     'Xero-tenant-id': tenant_id
        # }
        #
        # response = requests.get(url='https://api.xero.com/api.xro/2.0/Invoices', headers=headers)
        return request.redirect('/')
