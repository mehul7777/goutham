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
        so_id = ''
        for key, value in data_dict.items():
            # try:
            if key == 0:
                header_list.append(value)
            else:
                # so_id = ''
                print(value)
                order_reference = value[0]
                customer = value[1]
                invoice_address = value[2]
                delivery_address = value[3]
                customer_po = value[4]
                customer_reference = value[5]
                quotation_template = value[6]
                confirmation_date = value[7] or False
                can_be_used_for_forecast = value[8]
                pricelist = value[9]
                payment_terms = value[10]
                project_start_date = value[11] or False
                project_end_date = value[12] or False
                delivery_method = value[13]
                point_of_contact = value[14]
                point_of_contact_po = value[15]
                appear_on_pdf = value[16]
                notes = value[17]
                # order_lines_is_a_service = value[18]
                # order_lines_product = value[19]
                # order_lines_oem = value[20]
                # order_lines_description = value[21]
                # order_lines_ordered_quantity = value[22]
                # order_lines_delivered_quantity = value[23]
                # order_lines_invoiced_quantity = value[24]
                # order_lines_unit_of_measure = value[25]
                # order_lines_analytic_tags = value[26]
                # order_lines_warehouse = value[27]
                # order_lines_unit_price = value[28]
                # order_lines_taxes = value[29] or None
                # order_lines_discount = value[30]
                warehouse = value[18]
                shipping_policy = value[19]
                planned_date = value[20] or False
                requested_date = value[21] or False
                sales_person = value[22]
                project_manager = value[23]
                tags = value[24]
                sales_team = value[25]
                online_signature = value[26]
                online_payment = value[27]
                company = value[28]
                analytic_account = value[29]
                lead_or_opportunity = value[30]
                order_date = value[31] or False
                fiscal_position = value[32]
                status = value[33]
                invoice_status = value[34]
                source_document = value[35]

                # product_id = self.env['product.product'].search([('name', '=', order_lines_product)], limit=1)
                # product_uom_id = self.env['uom.uom'].search([('name', '=', order_lines_unit_of_measure)], limit=1)
                # analytic_tags_ids = self.env["account.analytic.tag"].search([('name', '=', order_lines_analytic_tags)], limit=1)
                # tax_id = self.env["account.tax"].search([('name', '=', order_lines_taxes)], limit=1)
                # order_lines_warehouse_id = self.env["stock.warehouse"].search([('name', '=', order_lines_warehouse)], limit=1)
                # print(analytic_tags_ids.ids, tax_id.ids)

                lst = []
                if order_reference:
                    # if order_lines_product:
                    #     if not product_id:
                    #         products_val = {
                    #             'name': order_lines_product
                    #         }
                    #         product_id = self.env['product.product'].create(products_val)
                    #
                    #     if not analytic_tags_ids:
                    #         analytic_tags_vals = {
                    #             'name': analytic_tags_ids
                    #         }
                    #         analytic_tags_ids = self.env['account.analytic.tag'].create(analytic_tags_vals)
                    #
                    #     so_line_vals = (0, 0, {
                    #         'is_service': True if order_lines_is_a_service == "True" else False,
                    #         'product_id': product_id[0].id,
                    #         'product_oem_code': order_lines_oem,
                    #         'name': order_lines_description,
                    #         'product_uom_qty': order_lines_ordered_quantity,
                    #         'warehouse_id': order_lines_warehouse_id.id,
                    #         'product_uom': product_uom_id.id,
                    #         'analytic_tag_ids': [(6, 0, analytic_tags_ids.ids)],
                    #         'price_unit': order_lines_unit_price,
                    #         'tax_id': [(6, 0, tax_id.ids)],
                    #         'discount': order_lines_discount,
                    #         # 'order_id': so_id.id
                    #     })
                    #     lst.append(so_line_vals)
                        # sol_id = self.env['sale.order.line'].create(so_line_vals)
                        # print("sol_id", sol_id)
                        # print(so_line_vals)

                    part_id = self.env["res.partner"].search([('name', '=', customer), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                    invoice_addr = self.env["res.partner"].search([('parent_id', '=', part_id.id), ("type", "=", 'invoice')], limit=1)
                    delivery_addr = self.env["res.partner"].search([('parent_id', '=', part_id.id), ("type", "=", 'delivery')], limit=1)
                    # part_invo_id = self.env["res.partner"].search([('name', '=', invoice_address)])
                    # part_ship_id = self.env["res.partner"].search([('name', '=', delivery_address)])
                    sale_ord_temp_id = self.env["sale.order.template"].search([('name', '=', quotation_template)], limit=1)
                    priceli_id = self.env["product.pricelist"].search([('name', '=', pricelist)], limit=1)
                    point_of_contact_id = self.env["res.partner"].search([('name', '=', point_of_contact), '|', ('active', '=', True), ('active', '=', False)], limit=1)

                    warehouse_id = self.env["stock.warehouse"].search([('name', '=', warehouse)], limit=1)
                    user_id = self.env["res.users"].search([('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                    project_manager_id = self.env["res.users"].search([('name', '=', project_manager), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                    team_id = self.env["crm.team"].search([('name', '=', sales_team)], limit=1)
                    company_id = self.env["res.company"].search([('name', '=', company)], limit=1)
                    fiscal_position_id = self.env["account.fiscal.position"].search([('name', '=', fiscal_position)], limit=1)
                    payment_term_id = self.env["account.payment.term"].search([('name', '=', payment_terms)], limit=1)
                    carrier_id = self.env["delivery.carrier"].search([('name', '=', delivery_method)], limit=1)
                    tag_ids = self.env["crm.tag"].search([('name', '=', tags)], limit=1)
                    analytic_account_id = self.env["account.analytic.account"].search([('name', '=', analytic_account), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                    opportunity_id = self.env["crm.lead"].search([('name', '=', lead_or_opportunity)], limit=1)

                    if not part_id:
                        cutomers_val = {
                            'name': customer
                        }
                        part_id = self.env['res.partner'].create(cutomers_val)

                    if not invoice_addr:
                        invoice_addr = part_id

                    if not delivery_addr:
                        delivery_addr = part_id

                    search_sale_order = self.env["sale.order"].search([('name', '=', order_reference)])

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
                        'can_be_used_for_forecast': True if can_be_used_for_forecast == "True" else False,
                        'point_contact': point_of_contact_id.id,
                        'point_of_contact_po': point_of_contact_po,
                        'appear_on_pdf': True if appear_on_pdf == "True" else False,
                        'notes': notes,
                        'warehouse_id': warehouse_id.id,
                        'picking_policy': shipping_policy,
                        'planned_date': planned_date,
                        'requested_date': requested_date,
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
                        # 'order_line': lst,
                    }
                    if search_sale_order:
                        so_id = self.env['sale.order'].write(so_val)
                    # if not search_sale_order:
                    #     so_id = self.env['sale.order'].create(so_val)
                    #     print("so_id", so_id)
                    #     print(so_val)
                    # else:
                    #     search_sale_order.write(so_val)
                # else:
                #     if order_lines_product:
                #         so_line_vals = (0, 0, {
                #             'is_service': True if order_lines_is_a_service == "True" else False,
                #             'product_id': product_id.id,
                #             'product_oem_code': order_lines_oem,
                #             'name': order_lines_description,
                #             'product_uom_qty': order_lines_ordered_quantity,
                #             'warehouse_id': order_lines_warehouse_id.id,
                #             'product_uom': product_uom_id.id,
                #             'analytic_tag_ids': [(6, 0, analytic_tags_ids.ids)],
                #             'price_unit': order_lines_unit_price,
                #             'tax_id': [(6, 0, tax_id.ids)],
                #             'discount': order_lines_discount,
                #             # 'order_id': so_id.id
                #         })
                #         if so_id:
                #             lst.append(so_line_vals)
                #             so_line_id = so_id.write({'order_line': lst})
                #             print(so_line_id)

