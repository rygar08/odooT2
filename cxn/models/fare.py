import uuid

from odoo import fields, models, api
from .constants import DIRECTION_OPTIONS


class FareType(models.Model):
    _name = 'cxn.fare_type'
    _description = 'Description'

    name = fields.Char()
    description = fields.Text()
    color = fields.Integer()
