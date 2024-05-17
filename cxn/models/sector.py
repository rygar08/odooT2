# -*- coding: utf-8 -*-
import json
import uuid
import pprint
import re
import dateutil.parser
from datetime import datetime

import requests

from odoo import models, fields, api
from odoo.exceptions import UserError
from camel_converter import dict_to_snake
from .rezdy_model import RzOrder
from . import rezdy_exceptions as rx


# class OrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     option_label = fields.Char(string='Option Label')
#     option_price = fields.Float(string='Option Price')
#     is_booking = fields.Boolean(string='Is Booking', store=True, compute='_compute_is_booking')
#
#     @api.depends('rbi_id')
#     def _compute_is_booking(self):
#         for rec in self:
#             is_booking = bool(rec.rbi_id)


class Sector(models.Model):
    _name = 'cxn.sector'
    _description = 'Booking Item'

    guid = fields.Char(default=lambda self: str(uuid.uuid4()), string='GUID')
    booking_item_id = fields.Many2one('cxn.booking_item', string='Booking Item')
    sect = fields.Integer()

    pickup_time = fields.Datetime()
    actual_pickup_time = fields.Datetime()
    pickup = fields.Char(string='Pickup Location')
    pickup_location = fields.Char(string='Pickup Location')
    pickup_type_id = fields.Many2one('cxn.stop_type', string='Pickup Type')
    pickup_id = fields.Many2one('cxn.stop', string='Pickup Location')

    connect_id = fields.Many2one('cxn.stop', string='Connect Location')
    connect_pickup_time = fields.Datetime()
    connect_drop_off_time = fields.Datetime()

    drop_off = fields.Char(string='Drop off Location')
    drop_off_location = fields.Char(string='Drop off Location')
    drop_off_type_id = fields.Many2one('cxn.stop_type', string='Drop off Type')
    drop_off_id = fields.Many2one('cxn.stop', string='Drop off Location')
    actual_drop_off_time = fields.Datetime()

    flight_date = fields.Datetime(string='Flight Date')
    flight_number = fields.Char(string='Flight Number')

    allocation_id = fields.Many2one('cxn.allocation', string='Allocation')
    allocation_helper_id = fields.Many2one('cxn.allocation', string='Helper Allocation')
    state_id = fields.Many2one('cxn.allocation_status', string='State')

    checked_in = fields.Boolean()
    checked_in_time = fields.Datetime(default=fields.Datetime.now)

    risk = fields.Boolean()
    notes = fields.Text()
    ftl_time = fields.Datetime()
    fare_id = fields.Many2one('cxn.fare_type', string='Fare Type')



class RezdyOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _default_order_number(self):
        # Generate a UUID and return it as a string
        return str(uuid.uuid4())

    # so_id = fields.Many2one(comodel_name='sale.order', string='Sale Order', required=True, ondelete='cascade')
    # order_number = fields.Char(string='Order Number', default=_default_order_number, readonly=True)
    is_rezdy_order = fields.Boolean(string='Is Rezdy Order')
    rezdy_status = fields.Selection([
        ('ABANDONED_CART', 'Abandoned Cart'),
        ('CANCELLED', 'Cancelled'),
        ('CONFIRMED', 'Confirmed'),
        ('NEW', 'New'),
        ('ON_HOLD', 'On Hold'),
        ('PENDING_CUSTOMER', 'Pending Customer'),
        ('PENDING_SUPPLIER', 'Pending Supplier'),
        ('PROCESSING', 'Processing')
    ], string='Status', default='NEW', required=True)
    supplier_ref = fields.Integer(string='Supplier ID')
    # supplier_name = fields.Char(string='Supplier Name')
    # supplier_alias = fields.Char(string='Supplier Alias')
    # reseller_ref = fields.Integer(string='Reseller ID')
    # reseller_name = fields.Char(string='Reseller Name')
    # reseller_alias = fields.Char(string='Reseller Alias')
    # currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    reseller_user_id = fields.Many2one(comodel_name='res.partner')
    total_amount = fields.Monetary(string='Total Amount')
    total_paid = fields.Monetary(string='Total Paid')
    total_due = fields.Monetary(string='Total Due')
    date_created = fields.Datetime(string='Date Created')
    date_confirmed = fields.Datetime(string='Date Confirmed')
    date_paid = fields.Datetime(string='Date Paid')
    date_reconciled = fields.Datetime(string='Date Reconciled')
    comments = fields.Text(string='Comments')
    internal_notes = fields.Text(string='Internal Notes')
    source = fields.Char(string='Source')
    reseller_source = fields.Char(string='Reseller Source')
    source_channel = fields.Char(string='Source Channel')
    reseller_comments = fields.Text(string='Reseller Comments')
    reseller_reference = fields.Char(string='Reseller Reference')
    commission = fields.Float(string='Commission')
    payment_option = fields.Selection([
        ("ALIPAY", "Alipay"),
        ("BANKTRANSFER", "Bank Transfer"),
        ("CASH", "Cash"),
        ("CREDITCARD", "Credit card"),
        ("EXTERNAL", "External"),
        ("INVOICE", "Invoice"),
        ("PAYPAL", "Paypal")
    ], string='Payment Option')

    rbi_ids = fields.One2many(comodel_name='rezdy.booking_item', inverse_name='sale_order_id', string='Booking Items')

    # CXN Booking fields
    bkg_id = fields.Integer(string='Booking ID')
    bkg_guid = fields.Char(string='Booking GUID')

    @api.model
    def rezdy_reservation(self, data):
        rz_order = RzOrder(dict_to_snake(data), self.env)
        rezdy_product = self.env['rezdy.product'].sudo()
        pax_attribute_id = self.env.ref('rezdy.product_attribute_pax')
        pav = self.env['product.attribute.value']
        ptav = self.env['product.template.attribute.value']
        sale_order = self.env['sale.order'].sudo()
        rezdy_booking_item = self.env['rezdy.booking_item'].sudo()
        # TODO: Reject order if no Order Items in Order or any other basic validations are encountered that can
        #  be checked before processing the request

        # Create Rezdy Order (sale.order)
        ro_vals = rz_order.vals()
        rezdy_order_id = sale_order.create(ro_vals)
        print(f"Rezdy Order ID: {rezdy_order_id.id}")

        # Create Rezdy Booking Item and sale order lines
        rbi_vals = {}
        sol_vals = []
        for prod in data.get('items', []):
            # Record Rezdy Booking Item (Product)
            rezdy_product_id = rezdy_product.search([('internal_code', '=', prod.get('externalProductCode'))])
            if not rezdy_product_id:
                raise rx.RezdyInvalidProduct(prod.get('externalProductCode', '(code not supplied'))
            rezdy_product_id.validate_order(rz_order)
            pickup_label = rezdy_product_id.booking_template_id.get_label('pickup')
            drop_off_label = rezdy_product_id.booking_template_id.get_label('drop_off')
            flight_number_label = rezdy_product_id.booking_template_id.get_label('flight_number')
            flt_date_label = rezdy_product_id.booking_template_id.get_label('flight_date')
            flt_time_label = rezdy_product_id.booking_template_id.get_label('flight_time')
            rbi_vals = {
                'sale_order_id': rezdy_order_id.id,
                # 'pickup': rz_order.location(pickup_label if rezdy_product_id.direction == 'In' else drop_off_label),
                # 'drop_off': rz_order.location(drop_off_label if rezdy_product_id.direction == 'In' else pickup_label),
                'pickup': rz_order.location(pickup_label),
                'drop_off': rz_order.location(drop_off_label),
                'rezdy_product_id': rezdy_product_id.id,
                'total_quantity': prod.get('quantity', 0),
                'amount': prod.get('amount'),
                'subtotal': prod.get('subtotal'),
                'total_item_tax': prod.get('total_item_tax'),
                'start_time': prod.get('startTime'),
                'start_time_local': prod.get('startTimeLocal'),
                'end_time': prod.get('endTime'),
                'end_time_local': prod.get('endTimeLocal'),
                'flight_number': rz_order.get_field_value(flight_number_label),
                'flight_date': rz_order.get_field_value(flt_date_label),
                'flight_time': rz_order.get_field_value(flt_time_label)
            }
            # Compute Flight Datetime
            # date_label = rezdy_product_id.booking_template_id.get_label('flight_date')
            # time_label = rezdy_product_id.booking_template_id.get_label('flight_time')
            try:
                date_val = dateutil.parser.parse(rz_order.get_field_value(flt_date_label)).strftime('%Y-%m-%d')
                time_val = dateutil.parser.parse(rz_order.get_field_value(flt_time_label)).strftime('%H:%M')
                rbi_vals['flight_datetime'] = f"{date_val} {time_val}"
            except ValueError:
                pass
            # Create BOOKING ITEM
            rbi_id = rezdy_booking_item.create(rbi_vals)
            print(f"Rezdy Booking Item ID: {rbi_id.id}")

            for attribute in prod.get('quantities', []):
                if attribute.get('value', 0) > 0:
                    pav_id = pav.search(
                        [('attribute_id', '=', pax_attribute_id.id), ('name', '=', attribute.get('optionLabel', ''))]
                    )
                    combination = ptav.search([
                        ('product_tmpl_id', '=', rezdy_product_id.product_tmpl_id.id),
                        ('attribute_id', '=', pax_attribute_id.id),
                        ('product_attribute_value_id', '=', pav_id.id)
                    ])
                    product_id = rezdy_product_id.product_tmpl_id._get_variant_id_for_combination(combination)
                    if not product_id:
                        raise Exception('Product Variant not found')
                    sol_vals.append((0, 0, {
                        'order_id': rezdy_order_id.id,
                        'product_id': product_id,
                        'product_uom_qty': attribute.get('value', 0),
                        'rbi_id': rbi_id.id
                    }))
        if not sol_vals:
            raise Exception('No quantities supplied')
        rezdy_order_id.write({'order_line': sol_vals})
        result = {"bookings": [{"orderNumber": rezdy_order_id.name}]}

        return result

    def _prepare_confirmation_values(self):
        res = super()._prepare_confirmation_values()
        bi_confirm_ids = self.rbi_ids.filtered(lambda s: s.state == 'draft')
        if bi_confirm_ids:
            bi_confirm_vals = []
            for bi in bi_confirm_ids:
                bi_confirm_vals.append((1, bi.id, {'state': 'pending'}))
            res['rbi_ids'] = bi_confirm_vals
        return res

    def rezdy_booking(self, data):
        self.ensure_one()
        # Finalize Rezdy Order (sale.order) confirming the booking
        if self.state in ['draft', 'sent']:
            try:
                self.sudo().action_confirm()
            except Exception:
                msg = Exception.message if hasattr(Exception, 'message') else 'Unknown Error'
                raise rx.RezdyInternalError(error_message=f"Failed to book {self.name} with error: {msg}")
        id_key = f"CxnBooking-{self.id}"
        self.sudo().with_delay(description=f"Place booking for order: {self.name}", identity_key=id_key).cxn_booking()
        result = {"bookings": [{"orderNumber": self.name}]}
        return result

    def rezdy_cancel(self, data):
        self.ensure_one()
        # Finalize Rezdy Order (sale.order) confirming the booking
        self.sudo().action_cancel()
        result = {"bookings": [{"orderNumber": self.name}]}
        return result

    @api.model
    def get_source_id(self):
        source_id = int(self.env['ir.config_parameter'].sudo().get_param('rezdy.cxn_source_id'))
        return self.env['rezdy.source'].sudo().search([('id', '=', source_id)])

    def btn_cxn_booking(self):
        for rec in self:
            id_key = f"CxnBooking-{rec.id}"
            rec.sudo().with_delay(description=f"Place booking for order: {rec.name}", identity_key=id_key).cxn_booking()

    def cxn_booking(self):
        pax_attribute_id = self.env.ref('rezdy.product_attribute_pax')
        cxn_account = 5505
        pay_method = 2
        domain = 10

        # TODO: Add logic to group the bi records into suppliers and then execute the booking creation against the
        #  correct supplier - TO BE INVESTIGATED
        for rec in self.filtered(lambda s: s.state in ['sale', 'done']):
            sql = "EXEC Rezdy_BkgInsert ?, ?, ?, ?"
            params = (cxn_account, pay_method, domain, rec.partner_shipping_id.email)
            rows = self.get_source_id().execute_query(sql, params)
            if not rows:
                raise rx.RezdyInternalError(f"Failed to book {rec.name}")
            rec.write({'bkg_id': rows[0][0], 'bkg_guid': rows[0][1]})
            for bi in rec.rbi_ids.filtered(lambda s: s.state == 'pending'):
                # Compute pax numbers
                cxn_adults = 0
                cxn_child = 0
                cxn_cons = 0
                for sol_id in bi.order_line_ids:
                    for ptvv_id in sol_id.product_id.product_template_variant_value_ids:
                        cxn_adults = ptvv_id.product_attribute_value_id.cxn_adult * sol_id.product_uom_qty
                        cxn_child = ptvv_id.product_attribute_value_id.cxn_child * sol_id.product_uom_qty
                        cxn_cons = ptvv_id.product_attribute_value_id.cxn_cons * sol_id.product_uom_qty

                extra_luggage = 0
                large_luggage = 0
                travel_class = 0
                flight_time = bi.flight_datetime if bi.flight_datetime else False
                flight_info = bi.flight_number or "Not Supplied"
                from_id = bi.pickup_ref
                to_id = bi.drop_off_ref
                trip_start = bi.start_time_local or False
                trip_end = bi.end_time_local or False
                book_msg = f"Erp Order Ref.: {rec.name}"
                booking_notes = '\n\n'.join([book_msg, rec.reseller_comments]) if rec.reseller_comments else book_msg
                travel_notes = rec.comments or '' if bi.flight_datetime else '\n\n'.join([
                    f"Agent/Customer supplied Flight Date: {bi.flight_date or 'None'} Time: {bi.flight_time or 'None'}",
                    rec.comments or ''
                ])
                sql = "EXEC Rezdy_BkgItemInsert ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
                params = (
                    rec.bkg_id,  # @BookingID int,
                    rec.partner_shipping_id.name,  # @Name varchar(255),
                    rec.partner_shipping_id.phone,  # @Phone varchar(255),
                    rec.reseller_reference or '',  # @Voucher varchar(255),
                    rec.reseller_user_id and rec.reseller_user_id.name[:50] or '',  # @AgentName varchar(50),
                    cxn_adults,  # @Adults int,
                    cxn_child,  # @Child int,
                    cxn_cons,  # @Cons int,
                    rec.total_amount,  # @Retail float,
                    rec.total_amount - rec.commission,  # @Nett float,
                    extra_luggage,  # @ExLug int
                    large_luggage,  # @LrgLug int
                    booking_notes[:500],  # @BookingNotes varchar(500)
                    travel_class,  # @TravelClass int
                    bi.rezdy_product_id.schedule_id[:10],  # @ScheduleId varchar(10)
                    from_id,  # @FromId varchar(10),    --eg. H123123 (hotel) or 343 (Allstop)
                    to_id,  # @ToId varchar(10),
                    flight_time,  # @FlightTime datetime
                    flight_info[:100],  # @FlightInfo varchar(100),
                    trip_start,  # @TripStart datetime
                    trip_end,  # @TripEnd datetime
                    travel_notes[:500]  # @TravelNotes varchar(500)
                )
                print('Flight Info:', flight_info[:100])
                pprint.pprint(params)
                rows = self.get_source_id().execute_query(sql, params)
                bi.write({'bkg_item_ref': rows[0][0], 'bkg_item_guid': rows[0][0], 'state': 'confirmed'})
                # Trigger Booking Confirmation Email
                domain_apikey = "A24AE6F5-EE01-43BA-AE89-BFFAC12D3921"
                url = f"https://dev.con-x-ion.com/app/Book2/Confirmation?api_key={bi.bkg_item_guid}"
                body = {'id': bi.bkg_item_guid, 'send': True, 'action': 'print'}
                requests.post(url, data=json.dumps(body), headers={'Content-Type': 'application/json'})
        return True
