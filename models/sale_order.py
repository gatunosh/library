# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    
    _inherit = 'sale.order'
    
    def action_confirm(self):
        '''
        Validamos que si el producto es libro solo se pueda alquilar si esta disponible
        Si esta disponible verifica que ya exista en el historico, si existe actualiza
        si no crea un nuevo registro en el historico para el libro
        '''
        for sale in self:
            res = super(SaleOrder, self).action_confirm()
            sale_order_line_only_book = self.env['sale.order']
            sale_order_line = sale.order_line
            sale_order_line_only_book = sale_order_line.filtered(lambda x: x.product_id.is_book == True)
            if sale_order_line_only_book:
                for book in sale_order_line_only_book:
                    if book.product_id.rent == 'rented':
                        raise UserError(u'EL libro %s no esta disponible para ser alquilado' % book.name)
                    rent = self.env['rent.order'].search([('product_id','=',book.product_id.id)])
                    if rent:
                        #Actualiza el registro en la tabla rent para el libro
                        rent_order_line_review = {
                            'user_rent_id': sale.user_rent_id.id,
                            'rent_id': rent.id,
                            'initial_rent_date': sale.initial_rent_date,
                            'final_rent_date': sale.final_rent_date
                        }
                        rent_order_line_create = self.env['rent.order.line'].create(rent_order_line_review)
                    else:
                        #Crea un nuevo registro en la tabla de rent para el libro
                        rent_review_create  = self.env['rent.order'].create({'product_id': book.product_id.id})
                        rent_order_line_review = {
                            'user_rent_id': sale.user_rent_id.id,
                            'rent_id': rent_review_create.id,
                            'initial_rent_date': sale.initial_rent_date,
                            'final_rent_date': sale.final_rent_date
                        }
                        rent_order_line_create = self.env['rent.order.line'].create(rent_order_line_review)
                    book.product_id.write({'rent':'rented'})
            return res
    
    user_rent_id = fields.Many2one(
        comodel_name = 'res.partner',
        copy = False,
        string = u'Cliente que alquila',
        help = u'Cliente que alquila el libro'
    )
    initial_rent_date = fields.Date(
        string = u'Fecha de alquiler',
        help = u'Fecha de alquiler sea crea automaticamente cuando se crea la orden',
        default = lambda self: fields.Datetime.now(),
        readonly = True,
        copy = False
    )
    final_rent_date = fields.Datetime(
        string = u'Fecha de entrega',
        help = u'Fecha de entrega del libro',
        copy = False
    )