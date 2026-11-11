from odoo import fields, models


class HpRestorationType(models.Model):
    _name = 'hp.restoration.type'
    _description = 'Restoration site type'
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
