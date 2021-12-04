from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class SOWizard(models.TransientModel):
    _name = "so.wizard"
    _description = "SO Wizard"

    load_file = fields.Binary("Load File")

    def import_so_data(self):
        print("Import is working")
        csv_data = self.load_file
        file_obj = TemporaryFile('wb+')
        csv_data = base64.decodebytes(csv_data)
        file_obj.write(csv_data)
        file_obj.seek(0)
        str_csv_data = file_obj.read().decode('utf-8')
        lis = csv.reader(io.StringIO(str_csv_data), delimiter=',')
        row_num = 0
        header_list = []
        data_dict = {}
        for row in lis:
            data_dict.update({row_num: row})
            row_num += 1
        for key, value in data_dict.items():
            # try:
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                order_reference = value[0]
                customer = value[1]
                invoice_address = value[2]
                delivery_address = value[3]
                customer_po = value[4]
                customer_reference = value[5]
                quotation_template = value[6]
                confirmation_date = value[7] or None
                pricelist = value[8]
                project_start_date = value[9] or None
                project_end_date = value[10] or None
                point_of_contact = value[11]
                order_lines_is_a_service = value[12]
                order_lines_product = value[13]
                order_lines_oem = value[14]
                order_lines_description = value[15]
                order_lines_ordered_quantity = value[16]
                order_lines_unit_of_measure = value[17]
                order_lines_analytic_tags = value[18]
                order_lines_warehouse = value[19]
                order_lines_unit_price = value[20]
                order_lines_taxes = value[21] or None
                order_lines_discount = value[22]
                warehouse = value[23]
                shipping_policy = value[24]
                sales_person = value[25]
                project_manager = value[26]
                sales_team = value[27]
                online_signature = value[28]
                online_payment = value[29]
                company = value[30]
                order_date = value[31] or None
                fiscal_position = value[32]
                status = value[33]
                invoice_status = value[34]
                source_document = value[35]
                payment_terms = value[36]
                delivery_method = value[37]
                tags = value[38]
                analytic_account = value[39]
                lead_or_opportunity = value[40]

                part_id = self.env["res.partner"].search([('name', '=', customer)])
                invoice_addr = self.env["res.partner"].search([('parent_id', '=', part_id.id), ("type", "=", 'invoice')], limit=1)
                delivery_addr = self.env["res.partner"].search([('parent_id', '=', part_id.id), ("type", "=", 'delivery')], limit=1)
                # part_invo_id = self.env["res.partner"].search([('name', '=', invoice_address)])
                # part_ship_id = self.env["res.partner"].search([('name', '=', delivery_address)])
                sale_ord_temp_id = self.env["sale.order.template"].search([('name', '=', quotation_template)])
                priceli_id = self.env["product.pricelist"].search([('name', '=', pricelist)])
                point_of_contact_id = self.env["res.partner"].search([('name', '=', point_of_contact)], limit=1)

                warehouse_id = self.env["stock.warehouse"].search([('name', '=', warehouse)])
                user_id = self.env["res.users"].search([('name', '=', sales_person)])
                project_manager_id = self.env["res.users"].search([('name', '=', project_manager)])
                team_id = self.env["crm.team"].search([('name', '=', sales_team)])
                company_id = self.env["res.company"].search([('name', '=', company)])
                fiscal_position_id = self.env["account.fiscal.position"].search([('name', '=', fiscal_position)])
                payment_term_id = self.env["account.payment.term"].search([('name', '=', payment_terms)])
                carrier_id = self.env["delivery.carrier"].search([('name', '=', delivery_method)])
                tag_ids = self.env["crm.tag"].search([('name', '=', tags)])
                analytic_account_id = self.env["account.analytic.account"].search([('name', '=', analytic_account)])
                opportunity_id = self.env["crm.lead"].search([('name', '=', lead_or_opportunity)])

                if status == "done":
                    if not part_id:
                        cutomers_val = {
                            'name': customer
                        }
                        part_id = self.env['res.partner'].create(cutomers_val)

                    if not invoice_addr:
                        invoice_addr = part_id

                    if not delivery_addr:
                        delivery_addr = part_id

                    if order_reference:
                        so_val = {
                            'name': order_reference,
                            'partner_id': part_id.id,
                            'partner_invoice_id': invoice_addr.id,
                            'partner_shipping_id': delivery_addr.id,
                            'customer_po': customer_po,
                            'client_order_ref': customer_reference,
                            'sale_order_template_id': sale_ord_temp_id.id,
                            'date_order': order_date,
                            'pricelist_id': priceli_id.id,
                            'project_start_date': project_start_date,
                            'project_end_date': project_end_date,
                            'point_of_contact': point_of_contact_id.id,
                            'warehouse_id': warehouse_id.id,
                            'picking_policy': shipping_policy,
                            'user_id': user_id.id,
                            'project_manager': project_manager_id.id,
                            'team_id': team_id.id,
                            'require_signature': online_signature,
                            'require_payment': online_payment,
                            'company_id': company_id.id,
                            'commitment_date': confirmation_date,
                            'fiscal_position_id': fiscal_position_id.id,
                            'state': status,
                            'invoice_status': invoice_status,
                            'origin': source_document,
                            'payment_term_id': payment_term_id.id,
                            'carrier_id': carrier_id.id,
                            'tag_ids': tag_ids.ids,
                            'analytic_account_id': analytic_account_id.id,
                            'opportunity_id': opportunity_id.id,
                        }
                        so_id = self.env['sale.order'].create(so_val)
                        print("so_id", so_id)
                        print(so_val)

                    product_id = self.env['product.product'].search([('name', '=', order_lines_product)])
                    product_uom_id = self.env['uom.uom'].search([('name', '=', order_lines_unit_of_measure)])
                    analytic_tags_ids = self.env["account.analytic.tag"].search([('name', '=', order_lines_analytic_tags)])
                    tax_id = self.env["account.tax"].search([('name', '=', order_lines_taxes)])
                    order_lines_warehouse_id = self.env["stock.warehouse"].search([('name', '=', order_lines_warehouse)])
                    print(analytic_tags_ids.ids, tax_id.ids)
                    if not product_id:
                        products_val = {
                            'name': order_lines_product
                        }
                        product_id = self.env['product.product'].create(products_val)

                    if not analytic_tags_ids:
                        analytic_tags_vals = {
                            'name': analytic_tags_ids
                        }
                        analytic_tags_ids = self.env['account.analytic.tag'].create(analytic_tags_vals)

                    so_line_vals = {
                        'is_service': order_lines_is_a_service,
                        'product_id': product_id[0].id,
                        'oem_code': order_lines_oem,
                        'name': order_lines_description,
                        'product_uom_qty': order_lines_ordered_quantity,
                        'warehouse_id': order_lines_warehouse_id.id,
                        'product_uom': product_uom_id.id,
                        'analytic_tag_ids': [(6, 0, analytic_tags_ids.ids)],
                        'price_unit': order_lines_unit_price,
                        'tax_id':  [(6, 0, tax_id.ids)],
                        'discount': order_lines_discount,
                        'order_id': so_id.id
                    }
                    sol_id = self.env['sale.order.line'].create(so_line_vals)
                    print("sol_id", sol_id)
                    print(so_line_vals)
        return True
