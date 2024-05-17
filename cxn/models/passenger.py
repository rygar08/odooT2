# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Passenger(models.Model):
    _inherit = 'res.partner'

    pay_token = fields.Char('Payment Token')
