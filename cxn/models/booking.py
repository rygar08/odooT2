# -*- coding: utf-8 -*-
import json
import uuid
import pprint
import re
import dateutil.parser
from datetime import datetime

import requests

from odoo import models, fields, api
from .constants import PAYMENT_OPTIONS
from odoo.exceptions import UserError
from camel_converter import dict_to_snake
from .rezdy_model import RzOrder
from . import rezdy_exceptions as rx


# class OrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     option_label = fields.Char(string='Option Label')
#     option_price = fields.Float(string='Option Price')
#     is_booking = fields.Boolean(string='Is Booking', store=True, compute='_compute_is_booking')
#
#     @api.depends('rbi_id')
#     def _compute_is_booking(self):
#         for rec in self:
#             is_booking = bool(rec.rbi_id)


class Booking(models.Model):
    _inherit = 'sale.order'

    guid = fields.Char(default=lambda self: str(uuid.uuid4()), string='GUID')
    account_id = fields.Many2one('account.account', string='Account')
    state = fields.Selection(selection=[('draft', 'New'), ('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancel', 'Cancelled')], required=True, default='draft')
    currency_id = fields.Many2one(comodel_name='res.currency', related='sale_order_id.currency_id', store=True)
    order_line_ids = fields.One2many('sale.order.line', 'order_id', string="Order Lines", readonly=True)
    domain_id = fields.Many2one('cxn.domain', string='Domain')
    passenger_id = fields.Many2one('res.partner', string='Passenger')
    promo_code = fields.Char(string='Promo Code')
    email = fields.Char(string='Email')


class BookingItem(models.Model):
    _inherit = 'sale.order.line'

    guid = fields.Char(default=lambda self: str(uuid.uuid4()), string='GUID')
    order_id = fields.Many2one('sale.order', string='Order')
    user_id = fields.Many2one('res.partner', string='User', default=lambda self: self.env.user.partner_id)
    state = fields.Selection([
        ('ABANDONED_CART', 'Abandoned Cart'),
        ('NEW', 'New'),
        ('PROCESSING', 'Processing'),
        ('CANCELLED', 'Cancelled'),
        ('CONFIRMED', 'Confirmed')
    ], string='Status', default='NEW', required=True)
    group_name = fields.Char(string='Group Name')
    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    voucher = fields.Char(string='Voucher')
    booked_by_id = fields.Many2one(comodel_name='res.partner')
    adults = fields.Integer(string='Adults')
    children = fields.Integer(string='Children')
    infants = fields.Integer(string='Infants')
    concessions = fields.Integer(string='Concessions')
    nett = fields.Monetary()
    retail = fields.Monetary()

    comments = fields.Text(string='Comments')
    payment_option = fields.Selection(PAYMENT_OPTIONS, string='Payment Option')
    is_return = fields.Boolean(string='Is Return')
    is_multi = fields.Boolean(string='Is Multi')
    is_return_draft = fields.Boolean(string='Is Return Draft')
    override_price = fields.Boolean(string='Override Price')
    override_price_reason = fields.Char(string='Override Price Reason')
    affiliate_id = fields.Many2one('cxn.affiliate', string='Affiliate')
    office_notes = fields.Text(string='Office Notes')

    large_lug_item_id = fields.Many2one('cxn.large_lug_item', string='Large Luggage Items')
    is_qb = fields.Boolean(string='Is Quick Booking')



class LargeLugItem(models.Model):
    _name = 'cxn.large_lug_item'
    _description = 'Large Luggage Item'

    booking_item_id = fields.Many2one('cxn.booking_item', string='Booking Item', index=True)
    surfboards = fields.Integer()
    golf_clubs = fields.Integer()
    bikes = fields.Integer()
    other = fields.Integer()
    other_description = fields.Char()
