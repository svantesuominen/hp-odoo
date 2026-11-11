from odoo import fields, models


class HpRestorationStage(models.Model):
    _name = 'hp.restoration.stage'
    _description = 'Restoration site stage'
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
