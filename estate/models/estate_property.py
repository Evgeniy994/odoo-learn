from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'

    type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman_id = fields.Many2one('res.partner', string='Salesman')  # How to use original 'salesman' from 'estate.property.type ?
    buyer_id = fields.Many2one('res.users', string='Buyer', default=lambda self: self.env.user, copy=False)  # How to use original 'buyer' from 'estate.property.type ?
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offer')
    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability', copy=False, default=date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Float('Garden area(sqm)')
    living_area = fields.Float('Living area(sqm)')
    total_area = fields.Float('Total area(sqm)', compute='_compute_total')
    active = fields.Boolean('Active', default=True)
    best_offer = fields.Float('Best offer', compute='_compute_best_offer')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Choose a side")
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new',
        help='State field')

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped('offer_ids.price'))
