from markupsafe import Markup

from odoo import api, fields, models

PERMIT_HTML = Markup(
    '<ul>'
    '<li><input type="checkbox"/> Landowner contract</li>'
    '<li><input type="checkbox"/> Restoration plan</li>'
    '<li><input type="checkbox"/> ELY statement</li>'
    '<li><input type="checkbox"/> Forest Centre</li>'
    '<li><input type="checkbox"/> Protection status</li>'
    '</ul>'
)


class HpRestorationSite(models.Model):
    _name = 'hp.restoration.site'
    _description = 'Restoration Site'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'code, id'

    code = fields.Char(
        string='HP-ID',
        copy=False,
        index=True,
        tracking=True,
    )
    name = fields.Char(tracking=True)
    related_site_id = fields.Many2one(
        'hp.restoration.site',
        string='Related site',
    )
    city_id = fields.Many2one('res.city', string='City')
    state_id = fields.Many2one(
        related='city_id.state_id',
        string='Region',
    )
    property_identifier_ids = fields.Many2many(
        'hp.property.identifier',
        string='Property identifiers',
    )
    map_url = fields.Char(string='Map link')
    area_ha = fields.Float(string='Area (ha)', digits=(16, 2))
    latitude = fields.Float(digits=(16, 6))
    longitude = fields.Float(digits=(16, 6))
    description = fields.Html()
    employee_id = fields.Many2one('hr.employee', string='Hiilipörssi lead', tracking=True)
    stage_id = fields.Many2one(
        'hp.restoration.stage',
        string='Stage',
        tracking=True,
        group_expand='_read_group_stage_ids',
    )
    type_id = fields.Many2one('hp.restoration.type', string='Site type')
    permit_html = fields.Html(
        string='Permits and documents',
        sanitize=False,
        default=lambda self: PERMIT_HTML,
    )
    partner_id = fields.Many2one('res.partner', string='Landowner')
    landowner_html = fields.Html(string='Landowner notes')
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    area_for_sale_ha = fields.Float(string='Area for sale (ha)', digits=(16, 2))
    area_sold_ha = fields.Float(string='Area sold (ha)', digits=(16, 2))
    area_remaining_ha = fields.Float(
        string='Area remaining (ha)',
        compute='_compute_area_remaining_ha',
        store=True,
        digits=(16, 2),
    )

    _code_unique = models.Constraint(
        'unique (code)',
        'The HP-ID must be unique.',
    )

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for site in self:
            site.display_name = site.name or site.code or self.env._('Restoration Site')

    @api.depends('area_for_sale_ha', 'area_sold_ha')
    def _compute_area_remaining_ha(self):
        for site in self:
            site.area_remaining_ha = site.area_for_sale_ha - site.area_sold_ha

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env['hp.restoration.stage'].search([])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'hp.restoration.site'
                )
        return super().create(vals_list)
