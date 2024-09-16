from odoo import fields, models, api


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'


    sale_person_id  = fields.Many2one('hr.employee')
        # related ="partner_id.x_studio_sale_person")