# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _

class GeoLog(models.Model):
    _name = "cxn.geo_log"
    _description = "Domain GPS Log"

    guid = fields.Char(string='GUID', default=lambda self: str(uuid.uuid4()), readonly=True)
    driver_id = fields.Many2one('res.partner', string='Driver')
    latitude = fields.Float()
    longitude = fields.Float()
    speed = fields.Float()
    accuracy = fields.Float()
    bearing = fields.Float()
    battery = fields.Float()
    batch_guid = fields.Char()
    action = fields.Char()
    activity = fields.Char()
    client_time = fields.Datetime()
    session_id = fields.Char()
    allocation_id = fields.Integer()
    route_item_id = fields.Char()



