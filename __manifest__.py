# -*- coding:utf-8 -*-

{
    'name': 'Library',
    'version':'1.0',
    'depends': [
        'sale_management'
    ],
    'author':'Adrian Lima',
    'category': 'Sales',
    'summary': 'Módulo de presupuesto para el alquiler de libros',
    'description': '''
        Módulo para alquilar libros
    ''',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/res_partner_category.xml',
        'report/rent_order.xml',
        'views/product_view.xml',
        'views/sale_order_view.xml',
        'views/rent_order_view.xml',
        'views/return_book_view.xml'
    ],
}