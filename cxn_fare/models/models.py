from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import fields, models
from odoo.odoo import api, _
from odoo.odoo.exceptions import UserError, ValidationError
from odoo.odoo.tools import float_is_zero, float_compare


class Fare(models.Model):
    _name = 'cxn.fare'
    _description = 'Fare'

    name = fields.Char(required=True)
    description = fields.Text(required=True)
    color = fields.Integer(required=True, help='Color of the fare')


class FarePrice(models.Model):
    _name = 'cxn.fare.price'
    _description = 'Fare Price'

    fare_id = fields.Many2one('cxn.fare', string='Fare', required=True)
    price = fields.Float(required=True, help='Price of the fare')
    company_id = fields.Many2one('res.company', string='Company', required=True)
    active = fields.Boolean(default=True, help='Check if the fare is active')


