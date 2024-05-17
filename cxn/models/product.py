# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(selection_add=[('transport', 'Transport Ticket'), ], ondelete={'transport': 'set service'})

    @api.onchange('detailed_type')
    def _onchange_type_event(self):
        if self.detailed_type == 'transport':
            self.invoice_policy = 'order'

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping['transport'] = 'service'
        return type_mapping
