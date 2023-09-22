from odoo import api, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_estate_property_sold(self):
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer_id.partner_id.id,
            'move_type': 'out_invoice',
        })
        if invoice:
            return invoice
        return super().action_estate_property_sold()
