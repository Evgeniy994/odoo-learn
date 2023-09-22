from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _order = 'id desc'

    type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user, copy=False)
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
        selection=[('new', 'NEW'), ('offer received', 'OFFER RECEIVED'), ('offer accepted', 'OFFER ACCEPTED'), ('sold', 'SOLD'), ('canceled', 'CANCELED')],
        required=True,
        copy=False,
        default='new',
        help='State field')

    _sql_constraints = [
        ('check_expected_price', 'check(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'check(selling_price > 0)', 'The selling price must be positive.'),
    ]

    @api.ondelete(at_uninstall=False)
    def _check_property_state(self):
        for record in self:
            if record.state in ('offer received', 'offer accepted', 'sold'):
                raise UserError('Only new and canceled properties can be canceled')

    def action_estate_property_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled property cannot be sold.')
            record.state = 'sold'

    def action_estate_property_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold property cannot be canceled.')
            record.state = 'canceled'

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.mapped('offer_ids.price'))
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'south'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
