
from odoo import api, fields, models, _, Command
from odoo.tools.misc import formatLang
from collections import defaultdict
import base64



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    show_part_number = fields.Boolean(string="Show Part Nubmer", default=False)
    show_sn_col = fields.Boolean(string="Show SN Column", default=False)
    show_part_number_col = fields.Boolean(string="Show Part Nubmer Column", default=False)
    with_tax = fields.Boolean(
        string='With Tax',
        required=False)

    type_id = fields.Many2one(
        comodel_name='sale.type',
        required=False)
    delivery_id = fields.Many2one(
        comodel_name='sale.delivery',
        required=False)

    shiping_id = fields.Many2one(
        comodel_name='sale.shipping',
        required=False)

    package_id = fields.Many2one(
        comodel_name='sale.package',
        required=False)

    origin_id = fields.Many2one(
        comodel_name='sale.origin',
        required=False)

    validity_id = fields.Many2one(
        comodel_name='sale.validaty',
        required=False)

    warranty_id = fields.Many2one(
        comodel_name='sale.warranty',
        required=False)
    
    po_ref = fields.Char(
        required=False)
    mail = fields.Char(
        string='Mail', 
        required=False)
    inf_bank_id = fields.Many2one(comodel_name="inf.bank", string="Bank Name", required=False, )

    part_of_machine_ids = fields.One2many(
        comodel_name='sale.part_of_machine',
        inverse_name='sale_order_id',
        compute='_compute_part_of_machine_ids',
        store=True,
        string='Part of machine'
    )
    is_required = fields.Boolean(
        string='Is_required', 
        required=False)

    # def action_cancel(self):
    #     self.filtered(lambda so: so.state != 'cancel').write({'state': 'cancel'})
    #     for order in self:
    #         if order.state == 'cancel':
    #             order.order_line.filtered(lambda l: l.qty_delivered > 0).write({'qty_delivered': 0})
                
    #     self.message_post(body="Sale Order canceled but related delivery orders are kept as is.")

    #     return True


    def get_part_of_machine(self):
        for lin in self.part_of_machine_ids:
            lin.unlink()
        for order in self.order_line:
            if order.product_template_id.part_of_machine and order.product_template_id.product_id:
                product = self.env['product.product'].search([('product_tmpl_id','=',order.product_template_id.product_id.id)])
                part = self.env['sale.part_of_machine'].create({
                    'sale_order_id':self.id,
                    'product_id':product.id,
                    'name':order.product_template_id.product_id.name,
                    'product_uom_qty':order.product_uom_qty,
                })

    def _get_part_of_machine(self,product_id,qty):
        bom_kit = self.env['mrp.bom']._bom_find(product_id, bom_type='phantom')[product_id]
        if bom_kit:
            boms, bom_sub_lines = bom_kit.explode(product_id, qty)
            print(bom_sub_lines)
            return bom_sub_lines
        else:
            return False
        # for rec in self:
        #     if product_id:
        #         return product_id.get_components()
        #     else:
        #         return False

    @api.depends('order_line','order_line.product_id')
    def _compute_part_of_machine_ids(self):
        for rec in self:
            data = [Command.clear()]
            if rec.order_line:
                for line in rec.order_line:
                    if line.product_id:
                        product_id = rec._get_part_of_machine(line.product_id,line.product_uom_qty)
                        if product_id:
                            for product in product_id:
                                    print(product[0].product_id.name)
                                    data.append(Command.create({
                                        'product_id': product[0].product_id.id,
                                        'name': product[0].product_id.display_name,
                                        'price_unit': product[0].product_id.list_price,
                                        'product_uom_qty':product[0].product_qty * line.product_uom_qty
                                    }))
            rec.part_of_machine_ids = data
            


    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({
            'with_tax': self.with_tax,
            'type_id': self.type_id.id,
            'delivery_id': self.delivery_id.id,
            'shiping_id': self.shiping_id.id,
            'package_id': self.package_id.id,
            'origin_id': self.origin_id.id,
            'validity_id': self.validity_id.id,
            'warranty_id': self.warranty_id.id,
            'po_ref': self.po_ref,
            'mail': self.mail,
            'inf_bank_id' :self.inf_bank_id.id

        })
        return res



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    part_number = fields.Char(
        string='Part Number'
    )
    part_number_encrypted = fields.Char(string='Encrypted Part Number', compute='_compute_part_number_encrypted',
                                        store=True)
    # this field used in report
    print_unit_price = fields.Boolean('Show Unit Price', default=True)

    @api.depends('part_number')
    def _compute_part_number_encrypted(self):
        for line in self:
            line.part_number_encrypted = base64.b64encode(line.part_number.encode('utf-8')).decode('utf-8') if line.part_number else False

    

    # product_id = fields.Many2one(
    #     compute='_compute_product_id',
    #     inverse='_inverse_product_id',
    #     store=True,
    # )

    
    @api.onchange('part_number')
    def _compute_product_id(self):
        for rec in self:
            if rec.part_number:
                part_number = rec.env['product.part_number'].search([
                    ('name','=',rec.part_number),
                    ('product_id','!=',False)
                ])
                rec.product_id = part_number.product_id.product_variant_id.id if part_number else False

    

    def _inverse_product_id(self):  # sourcery skip: assign-if-exp
        for rec in self:
            if not rec.part_number:
                if rec.product_id:
                    rec.part_number = rec.product_id.product_tmpl_id.part_number_ids[0].name if rec.product_id.product_tmpl_id.part_number_ids else False
                else:
                    rec.part_number = False
                

    @api.onchange('product_id')
    def onchange_product_id_part_number(self):  # sourcery skip: assign-if-exp
        for rec in self:
            if not rec.part_number:
                if rec.product_id:
                    rec.part_number = rec.product_id.product_tmpl_id.part_number_ids[0].name if rec.product_id.part_number_ids else False
                else:
                    rec.part_number = False

    def _prepare_procurement_values(self, group_id=False):
        """ Prepare specific key for moves or other components that will be created from a stock rule
        coming from a sale order line. This method could be override in order to add other custom key that could
        be used in move/po creation.
        """
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        # Use the delivery date if there is else use date_order and lead time
        values.update({
            'part_number': self.part_number,
        })
        return values

class Tax(models.Model):
    _inherit = 'account.tax'


    @api.model
    def _prepare_tax_totals(self, base_lines, currency, tax_lines=None):
        """ Compute the tax totals details for the business documents.
        :param base_lines:  A list of python dictionaries created using the '_convert_to_tax_base_line_dict' method.
        :param currency:    The currency set on the business document.
        :param tax_lines:   Optional list of python dictionaries created using the '_convert_to_tax_line_dict' method.
                            If specified, the taxes will be recomputed using them instead of recomputing the taxes on
                            the provided base lines.
        :return: A dictionary in the following form:
            {
                'amount_total':                 The total amount to be displayed on the document, including every total
                                                types.
                'amount_untaxed':               The untaxed amount to be displayed on the document.
                'formatted_amount_total':       Same as amount_total, but as a string formatted accordingly with
                                                partner's locale.
                'formatted_amount_untaxed':     Same as amount_untaxed, but as a string formatted accordingly with
                                                partner's locale.
                'groups_by_subtotals':          A dictionary formed liked {'subtotal': groups_data}
                                                Where total_type is a subtotal name defined on a tax group, or the
                                                default one: 'Untaxed Amount'.
                                                And groups_data is a list of dict in the following form:
                    {
                        'tax_group_name':                   The name of the tax groups this total is made for.
                        'tax_group_amount':                 The total tax amount in this tax group.
                        'tax_group_base_amount':            The base amount for this tax group.
                        'formatted_tax_group_amount':       Same as tax_group_amount, but as a string formatted accordingly
                                                            with partner's locale.
                        'formatted_tax_group_base_amount':  Same as tax_group_base_amount, but as a string formatted
                                                            accordingly with partner's locale.
                        'tax_group_id':                     The id of the tax group corresponding to this dict.
                    }
                'subtotals':                    A list of dictionaries in the following form, one for each subtotal in
                                                'groups_by_subtotals' keys.
                    {
                        'name':                             The name of the subtotal
                        'amount':                           The total amount for this subtotal, summing all the tax groups
                                                            belonging to preceding subtotals and the base amount
                        'formatted_amount':                 Same as amount, but as a string formatted accordingly with
                                                            partner's locale.
                    }
                'subtotals_order':              A list of keys of `groups_by_subtotals` defining the order in which it needs
                                                to be displayed
            }
        """

        # ==== Compute the taxes ====

        to_process = []
        for base_line in base_lines:
            to_update_vals, tax_values_list = self._compute_taxes_for_single_line(base_line)
            to_process.append((base_line, to_update_vals, tax_values_list))

        def grouping_key_generator(base_line, tax_values):
            source_tax = tax_values['tax_repartition_line'].tax_id
            return {'tax_group': source_tax.tax_group_id}

        global_tax_details = self._aggregate_taxes(to_process, grouping_key_generator=grouping_key_generator)

        tax_group_vals_list = []
        for tax_detail in global_tax_details['tax_details'].values():
            tax_group_vals = {
                'tax_group': tax_detail['tax_group'],
                'base_amount': tax_detail['base_amount_currency'],
                'tax_amount': round(tax_detail['tax_amount_currency']),
            }

            # Handle a manual edition of tax lines.
            if tax_lines is not None:
                matched_tax_lines = [
                    x
                    for x in tax_lines
                    if x['tax_repartition_line'].tax_id.tax_group_id == tax_detail['tax_group']
                ]
                if matched_tax_lines:
                    tax_group_vals['tax_amount'] = sum(x['tax_amount'] for x in matched_tax_lines)

            tax_group_vals_list.append(tax_group_vals)

        tax_group_vals_list = sorted(tax_group_vals_list, key=lambda x: (x['tax_group'].sequence, x['tax_group'].id))

        # ==== Partition the tax group values by subtotals ====

        amount_untaxed = global_tax_details['base_amount_currency']
        amount_tax = 0.0

        subtotal_order = {}
        groups_by_subtotal = defaultdict(list)
        for tax_group_vals in tax_group_vals_list:
            tax_group = tax_group_vals['tax_group']

            subtotal_title = tax_group.preceding_subtotal or _("Untaxed Amount")
            sequence = tax_group.sequence

            subtotal_order[subtotal_title] = min(subtotal_order.get(subtotal_title, float('inf')), sequence)
            groups_by_subtotal[subtotal_title].append({
                'group_key': tax_group.id,
                'tax_group_id': tax_group.id,
                'tax_group_name': tax_group.name,
                'tax_group_amount': tax_group_vals['tax_amount'],
                'tax_group_base_amount': tax_group_vals['base_amount'],
                'formatted_tax_group_amount': formatLang(self.env, round(tax_group_vals['tax_amount']), currency_obj=currency),
                'formatted_tax_group_base_amount': formatLang(self.env, round(tax_group_vals['base_amount']),
                                                              currency_obj=currency),
            })

        # ==== Build the final result ====

        subtotals = []
        for subtotal_title in sorted(subtotal_order.keys(), key=lambda k: subtotal_order[k]):
            amount_total = amount_untaxed + amount_tax
            subtotals.append({
                'name': subtotal_title,
                'amount': amount_total,
                'formatted_amount': formatLang(self.env, round(amount_total), currency_obj=currency),
            })
            amount_tax += sum(x['tax_group_amount'] for x in groups_by_subtotal[subtotal_title])

        amount_total = amount_untaxed + amount_tax

        display_tax_base = (len(global_tax_details['tax_details']) == 1 and currency.compare_amounts(
            tax_group_vals_list[0]['base_amount'], amount_untaxed) != 0) \
                           or len(global_tax_details['tax_details']) > 1

        return {
            'amount_untaxed': currency.round(amount_untaxed) if currency else amount_untaxed,
            'amount_total': currency.round(amount_total) if currency else amount_total,
            'formatted_amount_total': formatLang(self.env, round(amount_total), currency_obj=currency),
            'formatted_amount_untaxed': formatLang(self.env, round(amount_untaxed), currency_obj=currency),
            'groups_by_subtotal': groups_by_subtotal,
            'subtotals': subtotals,
            'subtotals_order': sorted(subtotal_order.keys(), key=lambda k: subtotal_order[k]),
            'display_tax_base': display_tax_base
        }
