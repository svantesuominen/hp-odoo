from odoo.tests import TransactionCase


class TestRestorationSite(TransactionCase):

    def test_create_site_assigns_code_and_remaining_area(self):
        partner = self.env['res.partner'].create({'name': 'Landowner'})
        contractor = self.env['res.partner'].create({'name': 'Contractor'})
        site = self.env['hp.restoration.site'].create({
            'name': 'Teerisuo',
            'partner_id': partner.id,
            'contractor_id': contractor.id,
            'area_ha': 40.0,
            'area_for_sale_ha': 40.0,
            'area_sold_ha': 10.0,
        })
        self.assertTrue(site.code.startswith('HP-'))
        self.assertEqual(site.area_remaining_ha, 30.0)
        self.assertEqual(site.partner_id, partner)
        self.assertEqual(site.contractor_id, contractor)
        self.assertIn('Landowner contract', site.permit_html)

    def test_kanban_and_map_views_load(self):
        site = self.env['hp.restoration.site']
        kanban = site.get_view(view_type='kanban')
        self.assertIn('default_group_by="stage_id"', kanban['arch'])
        site_list = site.get_view(view_type='list')
        self.assertIn('optional="show"', site_list['arch'])
        self.assertIn('optional="hide"', site_list['arch'])
        map_view = site.get_view(view_type='map')
        self.assertIn('<map', map_view['arch'])
        self.assertIn('latitude', map_view['arch'])
