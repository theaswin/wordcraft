{
    'name': 'Phase 4',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Custom',
    'summary': 'A custom module for Odoo',
    'description': 'This module adds custom functionality to Odoo.',
    'depends': ['base','account'],
    'data': [
            'views/analytic_account_view.xml',
    ],
    'installable': True,
    'application': True,
}