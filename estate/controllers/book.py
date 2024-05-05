from odoo import odoo
from odoo.odoo.http import route

class MyController(odoo.http.Controller):

    @route('/bookings', auth='public')
    def handler(self):
        return stuff()