{
    'name': 'Hiilipörssi Base',
    'version': '20.0.1.0.0',
    'category': 'Services',
    'summary': 'Installs the Community apps used by the Hiilipörssi prototype',
    'author': 'Hiilipörssi',
    'license': 'LGPL-3',
    'application': True,
    'depends': [
        'contacts',
        'crm',
        'sale_management',
        'account',
        'project',
        'purchase',
        'hr',
        'hp_restoration',
    ],
    'data': [
        'data/install_finnish.xml',
    ],
}
