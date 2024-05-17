# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _


class Domain(models.Model):
    _name = "cxn.domain"
    _description = "Domain"

    api_key = fields.Char(string='GUID', default=lambda self: str(uuid.uuid4()), readonly=True)
    name = fields.Char(string='Domain Name', required=True)
    website = fields.Char(string='website', required=True)
    active = fields.Boolean(default=True)
    layout_id = fields.Many2one('cxn.client_layout', string='Domain Config')
    host_header_ids = fields.One2many('cxn.domain_header', 'domain_id', string='Headers')
    affiliate_id = fields.Many2one('cxn.affiliate', string='Affiliate')
    promo_code = fields.Char(string='Promo Code')
    app_type = fields.Selection([(
        'ops', 'Ops'), ('agent', 'Agent'), ('web', 'Web'), ('schoolies', 'Schoolies'), ('kiosk', 'Kiosk'), ('api', 'API')],
        string='App Type', required=True)
    user_type = fields.Selection([('user', 'User'), ('none', 'None')], string='User Type', required=True)
    product_menu_id = fields.Many2one('product.template', string='Product Menu')
    auto_complete_config_id = fields.Many2one('cxn.autocomplete_config', string='AutoComplete Config')
    kiosk_id = fields.Many2one('cxn.kiosk', string='Kiosk')
    default_account_id = fields.Many2one('account.account', string='Default Account')


class Headers(models.Model):
    _name = 'cxn.domain_header'
    _description = 'Domain Header'

    domain_id = fields.Many2one('cxn.domain', string='Domain')
    name = fields.Char()
    active = fields.Boolean(default=True)


class ClientLayout(models.Model):
    _name = 'cxn.client_layout'
    _description = 'Client Layout'

    name = fields.Char(string='Name', required=True)
    bg_img = fields.Char(string='Background Image', required=True)
    home_url = fields.Char(string='Home URL', required=True)
    show_header = fields.Boolean(default=True)
    logo_url = fields.Char(required=True)
    favicon_url = fields.Char(required=True)
    banner_url = fields.Char(required=True)
    hide_concessions = fields.Boolean(default=False)
    styles = fields.Text()
    hash_routes = fields.Boolean(default=False, help='Use hash routes for the client')


class AutoCompleteConfig(models.Model):
    _name = 'cxn.autocomplete_config'
    _description = 'Auto Complete Config'

    name = fields.Char()
    allow_alt_sources = fields.Boolean(default=True)
    source = fields.Char()
    location = fields.Char()
    schedule = fields.Char()
