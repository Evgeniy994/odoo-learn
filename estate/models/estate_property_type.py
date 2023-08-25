from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'

    name = fields.Char('Type', required=True)
    salesman = fields.Many2one('res.partner', string='Salesman')
    buyer = fields.Many2one('res.users', string='Buyer', default=lambda self: self.env.user, copy=False)
