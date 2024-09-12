from odoo import fields, models, api


class SaleDelivery(models.Model):
    _name = 'sale.delivery'
    _description = 'Sale Delivery'

    name = fields.Char()
