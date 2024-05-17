# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _
from .constants import PAYMENT_OPTIONS


class Provider(models.Model):
    _name = 'cxn.provider'
    _description = 'Provider'

    name = fields.Char()











