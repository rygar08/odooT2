# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class CreditCardType(models.Model):
    _name = "cxn.credit_card_type"
    _description = "Credit card types"

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', _('Document type name must be unique')),
        ('positive_surcharge', 'CHECK(surcharge > 0)', _('The surcharge must be positive')),
    ]

    name = fields.Char(string='Domain Name', required=True)
    surcharge = fields.Float()



