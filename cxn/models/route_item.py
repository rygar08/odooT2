import uuid

from odoo import fields, models, api
from .constants import DIRECTION_OPTIONS


class RouteItem(models.Model):
    _name = 'cxn.route_item'
    _description = 'Description'

    guid = fields.Char(default=lambda self: str(uuid.uuid4()), string='GUID')



