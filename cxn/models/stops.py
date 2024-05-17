import uuid

from odoo import fields, models, api
from .constants import DIRECTION_OPTIONS


class Stop(models.Model):
    _name = 'cxn.stop'
    _description = 'Description'

    name = fields.Char()
    code = fields.Char()
    type_id = fields.Many2one('cxn.stop_type', string='Type')
    latitude = fields.Float()
    longitude = fields.Float()
    active = fields.Boolean(default=True)
    notes = fields.Text()


class StopType(models.Model):
    _name = 'cxn.stop_type'
    _description = 'StopType'

    name = fields.Char()
