# -*- coding: utf-8 -*-
{
    'name': "Oath2-ex",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/access_token_view.xml',
        'views/shopify_product_view.xml',
        'views/shopify_contact_view.xml',
        'views/shopify_order_view.xml',
        'views/xero_token_view.xml',
        'views/templates.xml',
        'views/res_config_views.xml',
        'wizard/fetch_shopify_view.xml',
    ],
    'assets': {
        'oath2_ex.js_package_assets': [
            'oath2_ex/static/js/index.js',
        ],
    }
}
