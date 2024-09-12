from odoo import models, fields, api ,exceptions
from datetime import datetime

class Shipping(models.Model):
    _name = 'sale.shipping'
    _rec_name = 'name'

    name = fields.Char(translate=True)


class Packing(models.Model):
    _name = 'sale.package'
    _rec_name = 'name'

    name = fields.Char(translate=True)


class Offer(models.Model):
    _name = 'sale.origin'
    _rec_name = 'name'

    name = fields.Char(translate=True)


class Validate(models.Model):
    _name = 'sale.validaty'
    _rec_name = 'name'

    name = fields.Char( translate=True)



class Warranty(models.Model):
    _name = 'sale.warranty'
    _rec_name = 'name'

    name = fields.Char( translate=True)