# -*- coding: utf-8 -*-
{
    'name': "estate",

    'summary': """
        
    """,

    'description': """
         
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",

    'category': 'Tutorials/Estate',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # 'depends': ['base_setup', 'onboarding', 'product', 'analytic', 'portal', 'digest'],
    'application': True,
    'installable': True,
    'data': [
        'views/property.xml',
        'views/menu.xml',
    ],
    'license': 'AGPL-3'
}
