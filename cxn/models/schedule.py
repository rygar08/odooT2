from odoo import fields, models

class Schedule(models.Model):
    _name = 'cxn.schedule'
    _description = 'Schedule'

    name = fields.Char()
    description = fields.Char('Description')
    code = fields.Char(size=5)
    active = fields.Boolean(default=True)
    inbound_code = fields.Char()
    outbound_code = fields.Char()
    lead_time = fields.Float(help='Lead time in hours', default=24)
    


class ScheduleAccess(models.Model):
    _name = 'cxn.schedule_access'
    _description = 'Schedule Access'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)


class ScheduleAccessItem(models.Model):
    _name = 'cxn.schedule_access_item'
    _description = 'Schedule Access Items'

    access_id = fields.Many2one('cxn.schedule_access', string='Access List', required=True)
    schedule_id = fields.Many2one('cxn.schedule', string='Schedule', required=True)
