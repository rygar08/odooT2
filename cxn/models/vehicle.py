from odoo.odoo import fields, models


class Vehicle(models.Model):
    _name = 'cxn.vehicle'
    _description = 'Vehicle'

    name = fields.Char()
    description = fields.Char('Description')
    plate = fields.Char('Plate')
    capacity = fields.Integer()
    active = fields.Boolean(default=True)



