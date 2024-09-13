from odoo import _, api, fields, models, Command


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'



    def _create_invoices(self, sale_orders):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoices(sale_orders)
        data  = [Command.clear()]
        if self.sale_order_ids:
            for line in self.sale_order_ids.part_of_machine_ids:
                data.append(Command.create({
                                    'product_id': line.product_id.id,
                                    'name': line.product_id.display_name,
                                    'price_unit': line.product_id.list_price,
                                    'product_uom_qty':line.product_uom_qty
                                }))
        
        invoice.part_of_machine_ids = data

        return invoice
