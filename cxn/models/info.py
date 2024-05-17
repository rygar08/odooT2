# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _


class Info(models.Model):
    _name = 'cxn.info'
    _description = 'Info'
    _description = 'Info'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(track_visibility='always')
    info = fields.Text(track_visibility='always')
    active = fields.Boolean(default=True)

