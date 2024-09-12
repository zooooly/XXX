from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Selection(
        string='Customer Type',
        selection=[
            ('distributors', 'Distributors'),
            ('final_customer', 'Final Customer.'),
        ],
        default='distributors'
    )

    customer_code = fields.Char(
        string='Customer Code',
    )
    customer_code_readonly = fields.Char(
        string='Customer Code Flag',
        compute='_compute_customer_code',
        required=False)

    @api.depends('customer_code')
    def _compute_customer_code(self):
        for com in self:
            com.customer_code_readonly = com.customer_code if com.customer_code else False
            # com.update({'ref': com.customer_code_readonly})

    @api.constrains('customer_type')
    def _check_customer_type(self):
        for rec in self:
            if rec.customer_type == 'distributors':
                rec.customer_code = rec.env['ir.sequence'].next_by_code('customer.distributors.code.sequence')
                rec.ref = rec.customer_code
            elif rec.customer_type == 'final_customer':
                rec.customer_code = rec.env['ir.sequence'].next_by_code('customer.final.code.sequence')
                rec.ref = rec.customer_code

    # @api.model
    # def create(self, vals):
    #     if self.customer_type:
    #         if self.customer_type == 'distributors':
    #             sequence = self.env['ir.sequence'].next_by_code('customer.distributors.code.sequence')
    #             vals['customer_code'] = sequence
    #         if self.customer_type == 'final_customer':
    #             sequence2 = self.env['ir.sequence'].next_by_code('customer.final.code.sequence')
    #             vals['customer_code'] = sequence2
    #     return super(ResPartner, self).create(vals)

    @api.model
    def create(self, values):
        result = super(ResPartner, self).create(values)
        if self.customer_rank == 1:
            if 'customer_type' in result:
                if result['customer_type'] == 'distributors':
                    result['customer_code'] = self.env['ir.sequence'].next_by_code('customer.distributors.code.sequence')
                elif result['customer_type'] == 'final_customer':
                    result['customer_code'] = self.env['ir.sequence'].next_by_code('customer.final.code.sequence')
        return result
