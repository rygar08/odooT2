from odoo.odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = 'Real Estate Property'
    _order = 'name'

    _sql_constraints = [
        ('Unique Name', 'UNIQUE(name)', 'The name of the property must be unique')
    ]

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area', store=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    seller_id = fields.Many2one('res.partner', string='Seller', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')


class EsatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
    property_ids = fields.Many2many('estate.property', string='Properties')


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(required=True)
    state = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused'), ('pending', 'Pending')], default='pending')
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer('Validity (days)', default=7)
    create_date = fields.Datetime(default=fields.Datetime.now)
