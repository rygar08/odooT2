import uuid

from odoo import fields, models, api
from .constants import DIRECTION_OPTIONS


class Allocation(models.Model):
    _name = 'cxn.allocation'
    _description = 'Description'

    name = fields.Char()
    guid = fields.Char(default=lambda self: str(uuid.uuid4()), string='GUID')
    trip = fields.Float(required=True)
    schedule = fields.Many2one('cxn.schedule', string='Schedule', required=True)
    trip_id = fields.Many2one('cxn.trip', string='Trip')
    direction = fields.Selection(DIRECTION_OPTIONS, string='Direction', required=True)
    driver_id = fields.Many2one('res.partner', string='Driver', required=True)
    vehicle_id = fields.Many2one('cxn.vehicle', string='Vehicle', required=True)
    state = fields.Selection([('open', 'Open'), ('limited', 'Limited'), ('locked', 'Locked')], default='limited',
                             help='Open: Available for book, Limited: Limited to assigned bus capacity or open, Locked: Not available to book')
    start_time = fields.Datetime()
    parent_id = fields.Many2one('cxn.allocation', string='Parent Allocation')
    trip_type = fields.Selection([('main', 'Main line'), ('helper', 'Helper')], default='main', string='Trip Type')
    driver_confirmed = fields.Boolean(default=False)

    # Route related fields
    build_hash = fields.Char()
    route_hash = fields.Char()
    link_id = fields.Many2one('cxn.route_item', help='Last stop of previous trip')
    link_to_id = fields.Many2one('cxn.route_item', help='Starting point of this trip')
    link_duration = fields.Integer(help='Duration from the previous trip')
    link_distance = fields.Float(help='Distance from the previous trip')

    distance = fields.Float(help='Total Distance, excluding the link distance')
    duration = fields.Float(help='Total Duration, excluding the link duration')
    notes = fields.Text()


class AllocationStatus(models.Model):
    _name = 'cxn.allocation_status'
    _description = 'AllocationStatus'

    name = fields.Char()
    
class DriverConfirm(models.Model):
    _name = 'cxn.driver_confirm'
    _description = 'DriverConfirm'

    driver_id = fields.Many2one('cxn.driver', string='Driver')
    travel_date = fields.Date(string='Travel Date')
    first_pickup_time = fields.Datetime(string='First Pickup Time')
    



