# -*- coding:utf-8 -*-
from odoo import api, models, fields

class RentOrder(models.Model):
    
    _name = 'rent.order'
    
    @api.depends('rent_order_line_ids')    
    def _compute__rent_main_data(self):
        '''
        Método para calcular el promedio de calificación total del libro
        y la fecha de la ultimo alquiler
        '''
        for book in self:
            grade = 0
            count = 0
            order_line_sort_ids = book.rent_order_line_ids.sorted(
                lambda line: line.final_rent_date,
                reverse = True
            )
            for rent_line in book.rent_order_line_ids:
                grade += rent_line.book_grade
                count += 1
            book.last_rent_date = order_line_sort_ids[0].final_rent_date
            book.average_book_grade = grade/count

    product_id = fields.Many2one(
        comodel_name = 'product.product',
        string = u'Producto',
        readonly = 'True',
        help = u'Id del libro alquilado',
        copy = False
    )
    rent_order_line_ids = fields.One2many(
        comodel_name = 'rent.order.line',
        inverse_name = 'rent_id',
        string = u'Lineas de la renta',
        help = u'Campo que apunta a las lineas de la renta'
    )
    last_rent_date = fields.Datetime(
        string = u'Fecha del ultimo alquiler',
        help = u'Campo calculado de la fecha de entrega del ultimo alquiler',
        readonly = True,
        compute='_compute__rent_main_data',
        copy = False
    )
    average_book_grade = fields.Integer(
        string = u'Calificación promedio del libro',
        readonly = True,
        copy = False,
        compute = '_compute__rent_main_data',
        help = u'Campo calculado de la calificación promedio del libro'
    )
    product_image = fields.Binary(
        string = u'Imagen del libro',
        required = False,
        related = 'product_id.image_1920',
        help = u'Imagen del libro referenciada desde el producto'
    )
    
class RentOrderLine(models.Model):
    
    _name = 'rent.order.line'
    
    def _compute_rent_order_count(self):
        '''
        Calcula el total de rent_orders y los coloca en la variable rent_order_count
        '''
        for order in self:
            rent_order_ids = self.env['rent.order'].search([])
            if rent_order_ids:
                order.rent_order_count = len(rent_order_ids)
    
    def return_book(self):
        '''
        Coloca el estado del libro en disponible
        '''
        self.book_id.rent = 'available'
        self.state = 'available'
        
    def action_view_rent(self):
        '''
        Este metodo dispara una acción para movernos a los historicos del alquiler
        '''
        action = self.env["ir.actions.actions"]._for_xml_id("library.action_open_rent_order")
        return action
    
    user_rent_id = fields.Many2one(
        comodel_name = 'res.partner',
        copy = False,
        string = u'Cliente que alquila',
        help = u'Cliente que alquila el libro'
    )
    rent_id = fields.Many2one(
        comodel_name = 'rent.order',
        string = u'Alquiler',
        help = u'Cabecera de las lineas de alquiler'
    )
    initial_rent_date = fields.Date(
        string = u'Fecha de alquiler',
        help = u'Fecha de alquiler sea crea automaticamente cuando se crea la orden',
        readonly = True,
        copy = False
    )
    final_rent_date = fields.Datetime(
        string = u'Fecha de entrega',
        help = u'Fecha de entrega del libro',
        readonly = True,
        copy = False
    )
    book_grade = fields.Integer(
        string = u'Calificación del libro',
        help = u'Calificación del libro de cada persona'
    )
    review = fields.Text(
        string = u'Critica del libro',
        help = u'Campo para almecenar la critica del usuario'
    )
    book_id = fields.Many2one(
        comodel_name = 'product.product',
        related = 'rent_id.product_id',
        string = u'Libro',
        help = u'El libro al que pertenece este line'
    )
    book_image = fields.Binary(
        string = u'Imagen del libro',
        required = False,
        related = 'book_id.image_1920',
        help = u'Imagen del libro obtenida desde el producto'
    )
    state = fields.Selection(
        selection=[
            ('rented','Rentado'),
            ('available','Disponible')
        ],
        default = 'rented',
        string = u'Estados',
        copy = False,
        help = u'Estados para regresar el libro'
    )
    rent_order_count = fields.Integer(
        string = u'Libros', 
        compute = '_compute_rent_order_count',
        help = u'Cuenta el total del historico de rentas'
    )
    
    
    
    
    