# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _


class Driver(models.Model):
    _name = 'cxn.driver'
    _inherit = 'res.partner'

    is_driver = fields.Boolean(string='Is Driver')
    category_id = fields.Many2one('cxn.driver_category', string='Driver Category')


class DriverCategory(models.Model):
    _name = 'cxn.driver_category'
    _description = 'DriverCategory'

    name = fields.Char()
    active = fields.Boolean(default=True)


class DriverLive(models.Model):
    _name = 'cxn.driver_live'
    _description = 'Drivers Live'

    created_by_id = fields.Many2one('res.partner', string='Driver', default=lambda self: self.env.user.partner_id)
    modified_by_id = fields.Many2one('res.partner', string='Modified By')



