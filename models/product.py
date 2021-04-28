# -*- coding:utf-8 -*-
from odoo import api, models, fields

class ProductProduct(models.Model):
    
    _inherit = 'product.product'
        
    def name_get(self):
        '''
        Cambiamos el nombre del producto a "Nombre del producto - isbn" solo si es un libro
        '''
        return [(tag.id, "%s: %s" % (tag.name, tag.isbn)) if tag.is_book else (tag.id, "%s" % (tag.name)) for tag in self]
    
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        '''
        Cambiamos el name search para que busque por isbn del libro
        '''
        if args is None:
            args = []
        domain = args + ['|', ('name', operator, name), ('isbn', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    is_book = fields.Boolean(
        string = u'¿Es libro?',
        default = False,
        copy = True,
        help = u'Campo verificar si el producto es un libro o no',
    )
    isbn = fields.Char(
        string = u'ISBN',
        help = u'Número estándar internacional del libro',
        copy = False
    )
    author_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = u'Autor',
        help = u'Autor del libro'
    )
    author_category_id = fields.Many2one(
        comodel_name = 'res.partner.category',
        string = u'Categoria autor',
        #default = lambda self: self.env.ref('library.category_author'),
        help = u'Categoria autor de los usuarios'
    )
    rent = fields.Selection(
        [
            ('available','Disponible'),
            ('rented','Alquilado')
        ],
        string = u'Alquiler',
        help = u'Si esta disponible de alquilar o esta alquilado',
        default = 'available'
    )
    