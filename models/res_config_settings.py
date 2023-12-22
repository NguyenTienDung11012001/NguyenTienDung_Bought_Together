from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    shopify_api_key = fields.Char('API Key', config_parameter='oath2_ex.shopify_api_key')
    shopify_secret_key = fields.Char('API Secret', config_parameter='oath2_ex.shopify_secret_key')
    shopify_api_version = fields.Char('API Version', config_parameter='oath2_ex.shopify_api_version')
    shopify_webhook_base_url = fields.Char('Webhook URL', config_parameter='oath2_ex.shopify_webhook_base_url')
    xero_client_id = fields.Char('Client ID', config_parameter='oath2_ex.xero_client_id')
    xero_client_secret = fields.Char('Client Secret', config_parameter='oath2_ex.xero_client_secret')