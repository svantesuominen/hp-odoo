from odoo.tests import TransactionCase

PROFILE_MODULES = [
    'contacts',
    'crm',
    'sale_management',
    'account',
    'project',
    'purchase',
    'hr',
    'hp_restoration',
]


class TestDependencies(TransactionCase):

    def test_profile_modules_are_installed(self):
        modules = self.env['ir.module.module'].search([
            ('name', 'in', PROFILE_MODULES),
        ])
        self.assertEqual(
            set(modules.mapped('name')),
            set(PROFILE_MODULES),
        )
        self.assertEqual(set(modules.mapped('state')), {'installed'})

    def test_finnish_language_is_installed(self):
        lang = self.env['res.lang'].search([('code', '=', 'fi_FI')])
        self.assertTrue(lang.active)
