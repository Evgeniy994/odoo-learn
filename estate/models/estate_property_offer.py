from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _rec_name = 'property_id'

    price = fields.Float('Price')
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Date deadline', compute='_compute_date', inverse='_inverse_date')
    salesman_id = fields.Many2one('res.partner', string='Salesman', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Offer status",
        copy=False)

    @api.depends('create_date', 'validity', 'date_deadline')
    def _compute_date(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_date(self):
        # for record in self:
        #     deadline = fields.Datetime.to_datetime(record.date_deadline)
        #     create_date = fields.Datetime.to_datetime(record.create_date)
        #     if int((deadline - create_date).days / 365) != record.validity:
        #         record.validity = int((deadline - create_date).days / 365)
        #
        # for record in self:
        #     deadline = fields.Datetime.to_datetime(record.date_deadline)
        #     create_date = fields.Datetime.to_datetime(record.create_date)
        #     difference = deadline - create_date
        #     if difference != record.validity:
        #         record.validity = difference

        for record in self:
            deadline = fields.Datetime.to_datetime(record.date_deadline)
            create_date = fields.Datetime.to_datetime(record.create_date)
            record.validity = deadline - create_date
