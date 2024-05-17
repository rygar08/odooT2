# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _


class ErrorLog(models.Model):
    _name = "cxn.error_log"
    _description = "Error Log"

    error = fields.Text()
    stack_trace = fields.Text()
    Url = fields.Char()