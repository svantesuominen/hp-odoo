{
    'name': 'Hiilipörssi Restoration Sites',
    'version': '20.0.1.0.0',
    'category': 'Services',
    'summary': 'Restoration site register for Hiilipörssi',
    'author': 'Hiilipörssi',
    'license': 'LGPL-3',
    'application': True,
    'depends': [
        'base_address_extended',
        'contacts',
        'hr',
        'mail',
    ],
    'data': [
        'security/ir.access.csv',
        'data/sequence.xml',
        'data/restoration_stage_data.xml',
        'data/restoration_type_data.xml',
        'views/restoration_stage_views.xml',
        'views/restoration_type_views.xml',
        'views/restoration_site_views.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hp_restoration/static/src/lib/leaflet/leaflet-src.esm.js',
            'hp_restoration/static/src/lib/leaflet/leaflet.css',
            'hp_restoration/static/src/map/**/*',
        ],
    },
}
