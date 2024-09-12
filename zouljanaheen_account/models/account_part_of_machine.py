from odoo import _, api, fields, models


class account_part_of_machine(models.Model):
    _name = 'account.part_of_machine'
    _description = 'Account Part Of Machine'


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

    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Order'
    )
