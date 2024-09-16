from odoo import fields, models, api


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'


    sale_person_id  = fields.Many2one('hr.employee')
        # related ="partner_id.x_studio_sale_person")





class res_partner(models.Model):
    _inherit = 'res.partner'

    date = fields.Date()
    name = fields.Char()
    vat = fields.Char()