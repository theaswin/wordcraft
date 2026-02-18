{
    'name': 'Customer Metric Dashboard',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Personalized view for customer sales metrics.',
    'depends': ['sale_management','sale', 'account', 'purchase','contacts'],
    'data': [
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'customer_metric_dashboard/static/src/scss/dashboard.scss',
            'customer_metric_dashboard/static/src/js/dashboard.js',
            'customer_metric_dashboard/static/src/xml/dashboard.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js',

        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
