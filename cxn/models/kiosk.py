# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api, _


class Kiosk(models.Model):
    _name = "cxn.kiosk"
    _description = "Kiosk"

    name = fields.Char('Domain Name', required=True)
    pickup_id = fields.Many2one('cxn.stop', 'Pickup Location')
    home_note = fields.Text('Home Note')
    ping_time = fields.Datetime('Last Ping Time')
    show_qr = fields.Boolean(default=True)
    confirmation_note = fields.Text('Confirmation Note')


class KioskZone(models.Model):
    _name = 'cxn.kiosk_zone'
    _description = 'KioskZone'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    domain_id = fields.Many2one('cxn.domain', 'Domain',required=True)
    from_price = fields.Float('From Price')
    product_id = fields.Many2one('product.template', 'Product')
    unavailable_message = fields.Text('Unavailable Message')
    stop_id = fields.Many2one('cxn.stop', 'Stop')


class KioskZoneStop(models.Model):
    _name = 'cxn.kiosk_zone_stop'
    _description = 'KioskZoneStop'

    sequence = fields.Integer('Sequence')
    kiosk_zone_id = fields.Many2one('cxn.kiosk_zone', 'Kiosk Zone', required=True)
    stop_id = fields.Many2one('cxn.stop', 'Stop', required=True)
    stop_name = fields.Char('Alternate Stop Name', help='Overrides the stop name')


class KioskZoneInfoLinks(models.Model):
    _name = 'cxn.kiosk_zone_info_links'
    _description = 'KioskZoneInfoLinks'

    zone_id = fields.Many2one('cxn.kiosk_zone', 'Zone', required=True)
    info_id = fields.Many2one('cxn.info', 'Info', required=True)


