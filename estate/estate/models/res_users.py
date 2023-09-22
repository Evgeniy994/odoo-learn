from odoo import api, fields, models


class ResUsersProperty(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2Many('estate.property', 'salesman_id', string='Properties')
