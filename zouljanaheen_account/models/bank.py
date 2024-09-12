from odoo import api, fields, models


class InformationBank(models.Model):
    _name = 'inf.bank'

    name = fields.Char(required=True)
    beneficiary = fields.Char('Beneficiary')
    benef_bank = fields.Char('Benef .Bank')
    iban = fields.Char('IBAN')
    swift_code = fields.Char('Swift Code')
