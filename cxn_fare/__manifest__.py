{
    'name': "cxn_fare",

    'summary': """

    """,

    'description': """

    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",

    'category': 'Cxn',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # 'depends': ['base_setup', 'onboarding', 'product', 'analytic', 'portal', 'digest'],
    'application': True,
    'installable': True,
    'data': [
        'views/fare.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
    ],
    'license': 'AGPL-3'
}
# -*- coding: utf-8 -*-
