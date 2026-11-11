from odoo import fields, models


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('map', 'Map')])

    def _get_view_info(self):
        return {'map': {'icon': 'location_on'}} | super()._get_view_info()
