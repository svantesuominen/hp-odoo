from odoo import fields, models


class HpPropertyIdentifier(models.Model):
    _name = 'hp.property.identifier'
    _description = 'Property identifier'
    _order = 'name'

    name = fields.Char(required=True)
    _name_unique = models.Constraint(
        'unique (name)',
        'This property identifier already exists.',
    )
