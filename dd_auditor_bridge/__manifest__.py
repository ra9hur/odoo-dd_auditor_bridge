{
    'name': 'D&D Auditor Bridge',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Seamless SSO from Odoo Vendor Bills to the D&D Auditor Web App',
    'author': 'Raghu Ramarao',
    'price': 0,
    'currency': 'EUR',
    'description': "Free connector that adds a 'Verify D&D Charges' button to Vendor Bills, "
                   "providing single sign-on to the D&D Auditor Web Application. Requires an "
                   "active paid subscription to the D&D Audit Web Application.",
    'images': ['static/description/main_screenshot.png'],
    'depends': ['account'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}