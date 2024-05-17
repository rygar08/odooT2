# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _
from .constants import PAYMENT_OPTIONS


class Mco(models.Model):
    _name = 'cxn.mco'
    _description = 'Mco'

    name = fields.Char(required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    payment_option = fields.Selection(PAYMENT_OPTIONS, string='Payment Option',required=True)
    amount = fields.Monetary(required=True)
    voucher = fields.Char()
    account_id = fields.Many2one('account.account', string='Account',required=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, required=True)
