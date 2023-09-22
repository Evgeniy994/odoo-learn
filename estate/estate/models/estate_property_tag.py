from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _order = 'name'

    name = fields.Char('Tag', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique.'),
    ]
