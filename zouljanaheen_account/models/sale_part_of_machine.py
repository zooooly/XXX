from odoo import _, api, fields, models


class SalePartOfMachine(models.Model):
    _name = 'sale.part_of_machine'
    _description = 'Sale Part of Machine'



    name = fields.Char(
        string='Description'
    )

    product_id = fields.Many2one(
        comodel_name='product.product', 
        string='Product'
    )

    product_uom_qty = fields.Float(
        string='Quantity',
        default=1.0,
    )

    price_unit = fields.Float(
        string='Unit Price'
    )

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Order'
    )
    
    
    
    