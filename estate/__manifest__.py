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
        'views/property_offer.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'reports/property.xml',
    ],
    'license': 'AGPL-3'
}
# -*- coding: utf-8 -*-
