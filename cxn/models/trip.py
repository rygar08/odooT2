from odoo import fields, models, api
from .constants import DIRECTION_OPTIONS

class Trip(models.Model):
    _name = 'cxn.trip'
    _description = 'Description'

    name = fields.Char()
    schedule_id = fields.Many2one('cxn.schedule', string='Schedule', required=True)
    time = fields.Float(string='Time')
    direction = fields.Selection(DIRECTION_OPTIONS, string='Direction')
