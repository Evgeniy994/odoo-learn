from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _rec_name = 'property_id'

    price = fields.Float('Price')
    salesman_id = fields.Many2one('res.partner', string='Salesman', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Offer status",
        copy=False)
