{
    'name': 'My Order',
    'depends': ['base','sale','stock'],
    'version': '17.0.1.0.0',
    'application': True,
    'license': 'LGPL-3',
    'summery': 'My Order',
    'category': '',
    'author': 'Renjini',
    'sequence': 10,

    'data': [
                 'security/ir.model.access.csv',
                 'views/my_order_menu.xml',
                 'views/my_order_view.xml',
                 'views/my_delivery_view.xml',

        ],
}