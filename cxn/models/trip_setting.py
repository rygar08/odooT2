# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _

class TripSetting(models.Model):
    _name = "cxn.trip_setting"
    _description = "Trip Setting"

    name = fields.Char(string='Name', required=True)




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




