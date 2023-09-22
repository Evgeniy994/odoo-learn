import math

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _rec_name = 'property_id'
    _order = 'price'

    price = fields.Float('Price')
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Date deadline', compute='_compute_date', inverse='_inverse_date', default=date.today())
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, copy=False)
    buyer_id = fields.Many2one('res.users', string='Buyer', default=lambda self: self.env.user, copy=False)
    property_id = fields.Many2one('estate.property', string='Property', ondelete='cascade', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Offer status",
        copy=False)

    _sql_constraints = [
        ('check_price', 'check(price > 0)', 'The price must be strictly positive.'),
    ]

    @api.model
    def create(self, vals):
        record = super(EstatePropertyOffer, self).create(vals)
        if record.property_id.best_offer > 0:
            record.property_id.state = 'offer received'

        if record.property_id.best_offer >= record.price:  # Need to upgrade _inverse don't working
            raise UserError(f'The offer must be higher than {record.property_id.best_offer}')
        return record

    @api.depends('create_date', 'validity', 'date_deadline')
    def _compute_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_date(self):
        for record in self:
            deadline = fields.Datetime.to_datetime(record.date_deadline)
            create_date = fields.Datetime.to_datetime(record.create_date)
            record.validity = math.ceil((deadline - create_date).total_seconds() / 86400)

    def action_confirm(self):
        if self.property_id.state == 'offer accepted':
            raise UserError('You can only accept one offer.')
        else:
            for record in self:
                expected_price = record.property_id.expected_price * 0.9
                if float_compare(record.price, expected_price, 1) <= 0:
                    raise ValidationError('The selling price must be more then 90% of expected price! You must reduce the expected price if you want to accept this offer.')
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.state = 'offer accepted'
            self.buyer_id = self.buyer_id  # Need to upgrade

    def action_cancel(self):
        self.status = 'refused'

    #  !!! Based on the picture in the lesson, this check should be in the accept button  !!!

    # @api.constrains('price')
    # def check_selling_price(self):
    #     for record in self:
    #         expected_price = record.property_id.expected_price * 0.9
    #         if float_compare(record.price, expected_price, 1) <= 0:
    #             raise ValidationError('The selling price mist be at least 90% of expected price! You must reduce the expected price if you want to accept this offer')
