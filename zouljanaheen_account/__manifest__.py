# -*- coding: utf-8 -*-
{
    'name': "Zouljanaheen Account Custom",

    'author': "Malaz",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/security.xml',
        # 'data/ir_sequence_data.xml',
        # 'views/res_partner_views.xml',
        # 'views/sale_type.xml',
        # 'views/shipping.xml',
        # 'views/sale_order.xml',
        # 'views/bank.xml',
        # 'views/sale_report.xml',
        'views/account_move_views.xml',
        # 'report/sale_order_document.xml',
        # 'report/elmakteb_so_report.xml'
    ],

}
