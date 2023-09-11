from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _order = 'sequence, name'

    name = fields.Char('Type', required=True)
    salesman = fields.Many2one('res.partner', string='Salesman')
    buyer = fields.Many2one('res.users', string='Buyer', default=lambda self: self.env.user, copy=False)
    property_ids = fields.One2many('estate.property', 'type_id')
    sequence = fields.Integer(string='Sequence')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer('Offer count', compute='_compute_count')

    @api.depends('offer_ids')
    def _compute_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # def action_view_offers(self):
    #     return {
    #         'name': _('Offer'),
    #         'res_mode': 'estate.estate_property_offer',
    #         'view_mode': 'list,form,tree',
    #         'context': {},
    #         'target': 'current',
    #         'type': 'ir.actions.act_window',
    #     }
