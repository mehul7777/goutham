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
        print("Sale order is working")
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
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                order_reference = value[0].strip()
                id = value[1]
                customer = value[2]
                customer_id = value[3]
                invoice_address = value[4]
                delivery_address = value[5]
                customer_po = value[6]
                customer_reference = value[7]
                quotation_template = value[8]
                can_be_used_for_forecast = value[9]
                confirmation_date = value[10] or False
                pricelist = value[11]
                payment_terms = value[12]
                project_start_date = value[13] or False
                project_end_date = value[14] or False
                shipping_account = value[15]
                delivery_method = value[16]
                point_of_contact = value[17]
                point_of_contact_id = value[18]
                point_of_contact_po = value[19]
                appear_on_pdf = value[20]
                notes = value[21]
                warehouse = value[22]
                shipping_policy = value[23]
                planned_date = value[24] or False
                requested_date = value[25] or False
                sales_person = value[26]
                project_manager = value[27]
                tags = value[28]
                sales_team = value[29]
                online_signature = value[30]
                online_payment = value[31]
                company = value[32]
                analytic_account = value[33]
                analytic_account_id = value[34]
                lead_or_opportunity = value[35]
                order_date = value[36] or False
                fiscal_position = value[37]
                invoice_status = value[38]
                ignore_exceptions = value[39]
                source_document = value[40]
                campaign = value[41]
                medium = value[42]
                source = value[43]
                validity_start_date = value[44] or False
                validity = value[45] or False

                warehouse_id = self.env["stock.warehouse"].search([('name', '=', warehouse)], limit=1)
                user_id = self.env["res.users"].search(
                    [('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                project_manager_id = self.env["res.users"].search(
                    [('name', '=', project_manager), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                team_id = self.env["crm.team"].search([('name', '=', sales_team)], limit=1)
                company_id = self.env["res.company"].search([('name', '=', company)], limit=1)
                fiscal_position_id = self.env["account.fiscal.position"].search([('name', '=', fiscal_position)],
                                                                                limit=1)
                payment_term_id = self.env["account.payment.term"].search([('name', '=', payment_terms)], limit=1)
                carrier_id = self.env["delivery.carrier"].search([('name', '=', delivery_method)], limit=1)
                tag_ids = self.env["crm.tag"].search([('name', '=', tags)], limit=1)
                analytic_account_id = self.env["account.analytic.account"].search(
                    [('name', '=', analytic_account), ('custom_id', '=', analytic_account_id), '|',
                     ('active', '=', True), ('active', '=', False)], limit=1)
                opportunity_id = self.env["crm.lead"].search([('name', '=', lead_or_opportunity)], limit=1)

                part_id = self.env["res.partner"].search(
                    [('name', '=', customer), ('id_custom', '=', customer_id), '|', ('active', '=', True),
                     ('active', '=', False)], limit=1)
                invoice_addr = self.env["res.partner"].search(
                    [('parent_id', '=', part_id.id), ("type", "=", 'invoice')], limit=1)
                if not invoice_addr:
                    invoice_addr = part_id

                delivery_addr = self.env["res.partner"].search(
                    [('parent_id', '=', part_id.id), ("type", "=", 'delivery')], limit=1)
                if not delivery_addr:
                    delivery_addr = part_id

                sale_ord_temp_id = self.env["sale.order.template"].search([('name', '=', quotation_template)], limit=1)
                priceli_id = self.env["product.pricelist"].search([('name', '=', pricelist)], limit=1)
                point_of_contact_id = self.env["res.partner"].search(
                    [('name', '=', point_of_contact), ('id_custom', '=', point_of_contact_id), '|',
                     ('active', '=', True), ('active', '=', False)], limit=1)
                campaign_id = self.env["utm.campaign"].search([('name', '=', campaign)])
                medium_id = self.env["utm.medium"].search([('name', '=', medium)])
                source_id = self.env["utm.source"].search([('name', '=', source)])

                search_sale_order = self.env["sale.order"].search(
                    [('name', '=', order_reference), ('custom_so_id', '=', id)])

                so_val = {
                    'custom_so_id': id,
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
                    'require_signature': True if online_signature == "True" else False,
                    'require_payment': True if online_payment == "True" else False,
                    'company_id': company_id.id,
                    'commitment_date': confirmation_date,
                    'fiscal_position_id': fiscal_position_id.id,
                    'invoice_status': invoice_status,
                    'origin': source_document,
                    'payment_term_id': payment_term_id.id,
                    'carrier_id': carrier_id.id,
                    'tag_ids': [(6, 0, tag_ids.ids)],
                    'analytic_account_id': analytic_account_id.id,
                    'opportunity_id': opportunity_id.id,
                    'campaign_id': campaign_id.id,
                    'medium_id': medium_id.id,
                    'source_id': source_id.id,
                    'x_studio_validity_start_date': validity_start_date,
                    'validity_date': validity,
                }
                if not search_sale_order:
                    so_id = self.env['sale.order'].create(so_val)
                    print("so_id", so_id)
                    print(so_val)

    def create_so_line_data(self):
        print("Sale order line is working")
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
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                sale_order_id = value[0]
                order_lines_is_a_service = value[1]
                order_lines_product = value[2]
                order_lines_internal_reference = value[3]
                order_lines_oem = value[4]
                order_lines_description = value[5]
                order_lines_ordered_quantity = value[6]
                order_lines_delivered_quantity = value[7]
                order_lines_invoiced_quantity = value[8]
                order_lines_unit_of_measure = value[9]
                order_lines_analytic_tags = value[10]
                order_lines_warehouse = value[11]
                order_lines_unit_price = value[12]
                order_lines_taxes = value[13] or None
                order_lines_discount = value[14]

                if not order_lines_product:
                    order_lines_product = 'Service'
                    order_lines_internal_reference = 'Service'
                product_id = False
                product_uom_id = self.env['uom.uom'].search([('name', '=', order_lines_unit_of_measure)], limit=1)
                product_count = self.env['product.product'].search_count(
                    [('name', '=', order_lines_product), '|', ('active', '=', True), ('active', '=', False)])
                if product_count:
                    if product_count > 1:
                        product_id = self.env['product.product'].search(
                            [('uom_id', '=', product_uom_id.id), ('name', '=', order_lines_product),
                             ('default_code', '=', order_lines_internal_reference), '|', ('active', '=', True),
                             ('active', '=', False)], limit=1)
                    else:
                        product_id = self.env['product.product'].search(
                            [('name', '=', order_lines_product), '|', ('active', '=', True), ('active', '=', False)], limit=1)

                analytic_tags_ids = self.env["account.analytic.tag"].search([('name', '=', order_lines_analytic_tags)],
                                                                            limit=1)
                tax_id = self.env["account.tax"].search([('name', '=', order_lines_taxes)], limit=1)
                order_lines_warehouse_id = self.env["stock.warehouse"].search([('name', '=', order_lines_warehouse)],
                                                                              limit=1)
                order_id = self.env["sale.order"].search([('custom_so_id', '=', sale_order_id)])
                lst = []
                if order_lines_product and product_id:
                    so_line_vals = {
                        'is_service': True if order_lines_is_a_service == "True" else False,
                        'product_id': product_id.id,
                        'product_oem_code': order_lines_oem,
                        'name': order_lines_description,
                        'product_uom_qty': order_lines_ordered_quantity,
                        'warehouse_id': order_lines_warehouse_id.id,
                        'product_uom': product_uom_id.id,
                        'analytic_tag_ids': [(6, 0, analytic_tags_ids.ids)],
                        'price_unit': order_lines_unit_price,
                        'tax_id': [(6, 0, tax_id.ids)],
                        'discount': order_lines_discount,
                        'display_type': 'line_note' if not order_lines_unit_of_measure else None,
                        'order_id': order_id.id
                    }
                    self.env["sale.order.line"].create(so_line_vals)
                else:
                    lst.append(order_lines_product)
                    order_id.write({'note': lst})

    def change_status_of_so(self):
        print("Change status of so is working")
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
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                id = value[0]
                order_reference = value[1]
                status = value[2]

                search_sale_order = self.env["sale.order"].search([('name', '=', order_reference), ('custom_so_id', '=', id)])

                if search_sale_order:
                    search_sale_order.write({'state': status})

        # search_sale_order_line = self.env["sale.order.line"].search([('product_id', '=', 10252)])
        #
        # if search_sale_order_line:
        #     search_sale_order_line.write({'product_uom_qty': 0.065})




    # def import_so_data(self):
    #     print("Import is working")
    #     csv_data = self.load_file
    #     file_obj = TemporaryFile('wb+')
    #     csv_data = base64.decodebytes(csv_data)
    #     file_obj.write(csv_data)
    #     file_obj.seek(0)
    #     str_csv_data = file_obj.read().decode('utf-8')
    #     lis = csv.reader(io.StringIO(str_csv_data), delimiter=',')
    #     row_num = 0
    #     header_list = []
    #     data_dict = {}
    #     for row in lis:
    #         data_dict.update({row_num: row})
    #         row_num += 1
    #     so_id = ''
    #     for key, value in data_dict.items():
    #         if key == 0:
    #             header_list.append(value)
    #         else:
    #             print(value)
    #             order_reference = value[0]
    #             customer = value[1]
    #             customer_id = value[2]
    #             invoice_address = value[3]
    #             delivery_address = value[4]
    #             customer_po = value[5]
    #             customer_reference = value[6]
    #             quotation_template = value[7]
    #             can_be_used_for_forecast = value[8]
    #             confirmation_date = value[9] or False
    #             pricelist = value[10]
    #             payment_terms = value[11]
    #             project_start_date = value[12] or False
    #             project_end_date = value[13] or False
    #             shipping_account = value[14]
    #             delivery_method = value[15]
    #             point_of_contact = value[16]
    #             point_of_contact_id = value[17]
    #             point_of_contact_po = value[18]
    #             appear_on_pdf = value[19]
    #             notes = value[20]
    #             order_lines_is_a_service = value[21]
    #             order_lines_product = value[22]
    #             order_lines_internal_reference = value[23]
    #             order_lines_oem = value[24]
    #             order_lines_description = value[25]
    #             order_lines_ordered_quantity = value[26]
    #             order_lines_delivered_quantity = value[27]
    #             order_lines_invoiced_quantity = value[28]
    #             order_lines_unit_of_measure = value[29]
    #             order_lines_analytic_tags = value[30]
    #             order_lines_warehouse = value[31]
    #             order_lines_unit_price = value[32]
    #             order_lines_taxes = value[33] or None
    #             order_lines_discount = value[34]
    #             warehouse = value[35]
    #             shipping_policy = value[36]
    #             planned_date = value[37] or False
    #             requested_date = value[38] or False
    #             sales_person = value[39]
    #             project_manager = value[40]
    #             tags = value[41]
    #             sales_team = value[42]
    #             online_signature = value[43]
    #             online_payment = value[44]
    #             company = value[45]
    #             analytic_account = value[46]
    #             lead_or_opportunity = value[47]
    #             order_date = value[48] or False
    #             fiscal_position = value[49]
    #             invoice_status = value[50]
    #             ignore_exceptions = value[51]
    #             source_document = value[52]
    #             campaign = value[53]
    #             medium = value[54]
    #             source = value[55]
    #             status = value[56]
    #
    #             # print(order_lines_product)
    #             if not order_lines_product:
    #                 order_lines_product = 'Service'
    #                 order_lines_internal_reference = 'Service'
    #
    #             product_id = self.env['product.product'].search([('name', '=', order_lines_product), ('default_code', '=', order_lines_internal_reference)], limit=1)
    #             product_uom_id = self.env['uom.uom'].search([('name', '=', order_lines_unit_of_measure)], limit=1)
    #             analytic_tags_ids = self.env["account.analytic.tag"].search([('name', '=', order_lines_analytic_tags)], limit=1)
    #             tax_id = self.env["account.tax"].search([('name', '=', order_lines_taxes)], limit=1)
    #             order_lines_warehouse_id = self.env["stock.warehouse"].search([('name', '=', order_lines_warehouse)], limit=1)
    #             # print(analytic_tags_ids.ids, tax_id.ids)
    #
    #             warehouse_id = self.env["stock.warehouse"].search([('name', '=', warehouse)], limit=1)
    #             user_id = self.env["res.users"].search(
    #                 [('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #             project_manager_id = self.env["res.users"].search(
    #                 [('name', '=', project_manager), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #             team_id = self.env["crm.team"].search([('name', '=', sales_team)], limit=1)
    #             company_id = self.env["res.company"].search([('name', '=', company)], limit=1)
    #             fiscal_position_id = self.env["account.fiscal.position"].search([('name', '=', fiscal_position)],
    #                                                                             limit=1)
    #             payment_term_id = self.env["account.payment.term"].search([('name', '=', payment_terms)], limit=1)
    #             carrier_id = self.env["delivery.carrier"].search([('name', '=', delivery_method)], limit=1)
    #             tag_ids = self.env["crm.tag"].search([('name', '=', tags)], limit=1)
    #             analytic_account_id = self.env["account.analytic.account"].search(
    #                 [('name', '=', analytic_account), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #             opportunity_id = self.env["crm.lead"].search([('name', '=', lead_or_opportunity)], limit=1)
    #
    #             lst = []
    #             if order_reference:
    #                 if order_lines_product:
    #                     so_line_vals = (0, 0, {
    #                         'is_service': True if order_lines_is_a_service == "True" else False,
    #                         'product_id': product_id.id,
    #                         'product_oem_code': order_lines_oem,
    #                         'name': order_lines_description,
    #                         'product_uom_qty': order_lines_ordered_quantity,
    #                         'warehouse_id': order_lines_warehouse_id.id,
    #                         'product_uom': product_uom_id.id,
    #                         'analytic_tag_ids': [(6, 0, analytic_tags_ids.ids)],
    #                         'price_unit': order_lines_unit_price,
    #                         'tax_id': [(6, 0, tax_id.ids)],
    #                         'discount': order_lines_discount,
    #                         # 'display_type': 'line_note',
    #                         # 'order_id': so_id.id
    #                     })
    #                     print("so_line_vals1", so_line_vals)
    #                     lst.append(so_line_vals)
    #
    #                 part_id = self.env["res.partner"].search([('name', '=', customer), ('id_custom', '=', customer_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #                 invoice_addr = self.env["res.partner"].search([('parent_id', '=', part_id.id), ("type", "=", 'invoice')], limit=1)
    #                 if not invoice_addr:
    #                     invoice_addr = part_id
    #
    #                 delivery_addr = self.env["res.partner"].search([('parent_id', '=', part_id.id), ("type", "=", 'delivery')], limit=1)
    #                 if not delivery_addr:
    #                     delivery_addr = part_id
    #
    #                 sale_ord_temp_id = self.env["sale.order.template"].search([('name', '=', quotation_template)], limit=1)
    #                 priceli_id = self.env["product.pricelist"].search([('name', '=', pricelist)], limit=1)
    #                 point_of_contact_id = self.env["res.partner"].search([('name', '=', point_of_contact), ('id_custom', '=', point_of_contact_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #                 campaign_id = self.env["utm.campaign"].search([('name', '=', campaign)])
    #                 medium_id = self.env["utm.medium"].search([('name', '=', medium)])
    #                 source_id = self.env["utm.source"].search([('name', '=', source)])
    #
    #                 search_sale_order = self.env["sale.order"].search([('name', '=', order_reference)])
    #
    #                 so_val = {
    #                     'name': order_reference,
    #                     'partner_id': part_id.id,
    #                     'partner_invoice_id': invoice_addr.id,
    #                     'partner_shipping_id': delivery_addr.id,
    #                     'customer_po': customer_po,
    #                     'client_order_ref': customer_reference,
    #                     'sale_order_template_id': sale_ord_temp_id.id,
    #                     'date_order': order_date,
    #                     'pricelist_id': priceli_id.id,
    #                     'project_start_date': project_start_date,
    #                     'project_end_date': project_end_date,
    #                     'can_be_used_for_forecast': True if can_be_used_for_forecast == "True" else False,
    #                     'point_contact': point_of_contact_id.id,
    #                     'point_of_contact_po': point_of_contact_po,
    #                     'appear_on_pdf': True if appear_on_pdf == "True" else False,
    #                     'notes': notes,
    #                     'warehouse_id': warehouse_id.id,
    #                     'picking_policy': shipping_policy,
    #                     'planned_date': planned_date,
    #                     'requested_date': requested_date,
    #                     'user_id': user_id.id,
    #                     'project_manager': project_manager_id.id,
    #                     'team_id': team_id.id,
    #                     'require_signature': online_signature,
    #                     'require_payment': online_payment,
    #                     'company_id': company_id.id,
    #                     'commitment_date': confirmation_date,
    #                     'fiscal_position_id': fiscal_position_id.id,
    #                     'state': status,
    #                     'invoice_status': invoice_status,
    #                     'origin': source_document,
    #                     'payment_term_id': payment_term_id.id,
    #                     'carrier_id': carrier_id.id,
    #                     'tag_ids': [(6, 0, tag_ids.ids)],
    #                     'analytic_account_id': analytic_account_id.id,
    #                     'opportunity_id': opportunity_id.id,
    #                     'campaign_id': campaign_id.id,
    #                     'medium_id': medium_id.id,
    #                     'source_id': source_id.id,
    #                     'order_line': lst,
    #                 }
    #                 if not search_sale_order:
    #                     so_id = self.env['sale.order'].create(so_val)
    #                     print("so_id", so_id)
    #                     print(so_val)
    #             else:
    #                 if order_lines_product:
    #                     so_line_vals = (0, 0, {
    #                         'is_service': True if order_lines_is_a_service == "True" else False,
    #                         'product_id': product_id.id,
    #                         'product_oem_code': order_lines_oem,
    #                         'name': order_lines_description,
    #                         'product_uom_qty': order_lines_ordered_quantity,
    #                         'warehouse_id': order_lines_warehouse_id.id,
    #                         'product_uom': product_uom_id.id,
    #                         'analytic_tag_ids': [(6, 0, analytic_tags_ids.ids)],
    #                         'price_unit': order_lines_unit_price,
    #                         'tax_id': [(6, 0, tax_id.ids)],
    #                         'discount': order_lines_discount,
    #                         # 'order_id': so_id.id
    #                     })
    #                     if so_id:
    #                         lst.append(so_line_vals)
    #                         so_line_id = so_id.write({'order_line': lst})
    #                         print(so_line_id)
    #
