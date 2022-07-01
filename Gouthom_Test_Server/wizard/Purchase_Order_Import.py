from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class PO1Wizard(models.TransientModel):
    _name = "po1.wizard"
    _description = "PO1 Wizard"

    load_file = fields.Binary("Load File")

    def import_po1_data(self):
        print("purchase order is working")
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
            print(data_dict.items())
            if key == 0:
                header_list.append(value)
            else:
                # print(value)
                order_reference = value[0]
                id = value[1]
                vendor = value[2]
                vendor_id = value[3]
                vendor_reference = value[4]
                currency = value[5]
                order_date = value[6] or False
                scheduled_date = value[7] or False
                purchase_representative = value[8]
                billing_status = value[9]
                company = value[10]
                approval_date = value[11] or False
                deliver_to = value[12]
                deliver_to_warehouse = value[13]
                incoterm = value[14]
                source_sale_order = value[15]
                payment_terms = value[16]
                fiscal_position = value[17]

                c_id = self.env['res.currency'].search([('name', '=', currency)], limit=1)
                part_id = self.env['res.partner'].search(
                    [('name', '=', vendor), ('id_custom', '=', vendor_id), '|', ('active', '=', True),
                     ('active', '=', False)], limit=1)
                use_id = self.env['res.users'].search(
                    [('name', '=', purchase_representative), '|', ('active', '=', True), ('active', '=', False)],
                    limit=1)
                com_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                pick_type_id = self.env['stock.picking.type'].search([('name', '=', deliver_to)], limit=1)
                fis_pos_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position)], limit=1)
                incoterm_id = self.env['account.incoterms'].search([('name', '=', incoterm)], limit=1)
                payment_term_id = self.env['account.payment.term'].search([('name', '=', payment_terms)], limit=1)

                search_purchase_order = self.env['purchase.order'].search([('name', '=', order_reference), ('custom_po_id', '=', id)])

                po_order_val = {
                    'custom_po_id': id,
                    'name': order_reference,
                    'partner_id': part_id.id,
                    'partner_ref': vendor_reference,
                    'currency_id': c_id.id,
                    'date_order': order_date,
                    'date_planned': scheduled_date,
                    'user_id': use_id.id,
                    'invoice_status': billing_status,
                    'company_id': com_id.id,
                    'picking_type_id': pick_type_id.id,
                    'fiscal_position_id': fis_pos_id.id,
                    'date_approve': approval_date,
                    'incoterm_id': incoterm_id.id,
                    'payment_term_id': payment_term_id.id,
                }
                if not search_purchase_order:
                    po_id = self.env['purchase.order'].create(po_order_val)
                    print(po_id)

    def create_po1_line_data(self):
        print("Purchase order line is working")
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
            print(data_dict.items())
            if key == 0:
                header_list.append(value)
            else:
                # print(value)
                purchase_order_id = value[0]
                order_lines_product = value[1]
                order_lines_internal_reference = value[2]
                order_lines_description = value[3]
                order_lines_scheduled_date = value[4] or False
                order_lines_company = value[5]
                order_lines_analytic_account = value[6]
                order_lines_analytic_tags = value[7]
                order_lines_quantity = value[8]
                order_lines_unit_of_measure = value[9]
                order_lines_price_unit = value[10]
                order_lines_taxes = value[11]

                if not order_lines_product:
                    order_lines_product = 'Service'
                    order_lines_internal_reference = 'Service'

                if not order_lines_analytic_account:
                    order_lines_analytic_account = 'NOT DEFINE'

                # pro_id = self.env['product.product'].search(
                #     [('name', '=', order_lines_product), ('default_code', '=', order_lines_internal_reference), '|',
                #      ('active', '=', True), ('active', '=', False)], limit=1)
                pro_id = False
                product_uom_id = self.env['uom.uom'].search([('name', '=', order_lines_unit_of_measure)], limit=1)
                product_count = self.env['product.product'].search_count(
                    [('name', '=', order_lines_product), '|', ('active', '=', True), ('active', '=', False)])
                if product_count:
                    if product_count > 1:
                        pro_id = self.env['product.product'].search(
                            [('uom_id', '=', product_uom_id.id), ('name', '=', order_lines_product),
                             ('default_code', '=', order_lines_internal_reference), '|', ('active', '=', True),
                             ('active', '=', False)], limit=1)
                    else:
                        pro_id = self.env['product.product'].search(
                            [('name', '=', order_lines_product), '|', ('active', '=', True), ('active', '=', False)], limit=1)

                account_analytic_id = self.env['account.analytic.account'].search(
                    [('name', '=', order_lines_analytic_account), '|', ('active', '=', True), ('active', '=', False)],
                    limit=1)
                tax_id = self.env['account.tax'].search([('name', '=', order_lines_taxes)], limit=1)
                analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', order_lines_analytic_tags)])

                order_id = self.env["purchase.order"].search([('custom_po_id', '=', purchase_order_id)])

                lst = []
                if order_id:
                    if order_lines_product and pro_id:
                        po_line_vals = {
                            'product_id': pro_id.id,
                            'name': order_lines_description,
                            'date_planned': order_lines_scheduled_date,
                            'account_analytic_id': account_analytic_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                            'product_qty': order_lines_quantity,
                            'product_uom': product_uom_id.id,
                            'price_unit': order_lines_price_unit,
                            'taxes_id': [(6, 0, tax_id.ids)],
                            'display_type': "line_note" if not order_lines_unit_of_measure else None,
                            'order_id': order_id.id
                        }
                        self.env["purchase.order.line"].create(po_line_vals)
                    else:
                        lst.append(order_lines_product)
                        order_id.write({'notes': lst})

    def change_status_of_po(self):
        print("Change status of po is working")
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

                search_purchase_order = self.env["purchase.order"].search([('custom_po_id', '=', id)])

                if search_purchase_order:
                    search_purchase_order.write({'state': status})

    # def import_po1_data(self):
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
    #     po_id = ''
    #     for key, value in data_dict.items():
    #         print(data_dict.items())
    #         if key == 0:
    #             header_list.append(value)
    #         else:
    #             # print(value)
    #             order_reference = value[0]
    #             vendor = value[1]
    #             vendor_id = value[2]
    #             vendor_reference = value[3]
    #             currency = value[4]
    #             order_date = value[5] or False
    #             scheduled_date = value[6] or False
    #             purchase_representative = value[7]
    #             billing_status = value[8]
    #             company = value[9]
    #             approval_date = value[10] or False
    #             order_lines_product = value[11]
    #             order_lines_internal_reference = value[12]
    #             order_lines_description = value[13]
    #             order_lines_scheduled_date = value[14] or False
    #             order_lines_company = value[15]
    #             order_lines_analytic_account = value[16]
    #             order_lines_analytic_tags = value[17]
    #             order_lines_quantity = value[18]
    #             order_lines_unit_of_measure = value[19]
    #             order_lines_price_unit = value[20]
    #             order_lines_taxes = value[21]
    #             deliver_to = value[22]
    #             incoterm = value[23]
    #             source_sale_order = value[24]
    #             payment_terms = value[25]
    #             fiscal_position = value[26]
    #             status = value[27]
    #
    #             # print(order_lines_product)
    #             if not order_lines_product:
    #                 order_lines_product = 'Service'
    #                 order_lines_internal_reference = 'Service'
    #
    #             if not order_lines_analytic_account:
    #                 order_lines_analytic_account = 'NOT DEFINE'
    #
    #             c_id = self.env['res.currency'].search([('name', '=', currency)], limit=1)
    #             part_id = self.env['res.partner'].search([('name', '=', vendor), ('id_custom', '=', vendor_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #             use_id = self.env['res.users'].search([('name', '=', purchase_representative), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #             com_id = self.env['res.company'].search([('name', '=', company)], limit=1)
    #             pro_id = self.env['product.product'].search([('name', '=', order_lines_product), ('default_code', '=', order_lines_internal_reference), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #             pick_type_id = self.env['stock.picking.type'].search([('name', '=', deliver_to)], limit=1)
    #             fis_pos_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position)], limit=1)
    #             tax_id = self.env['account.tax'].search([('name', '=', order_lines_taxes)], limit=1)
    #             incoterm_id = self.env['account.incoterms'].search([('name', '=', incoterm)], limit=1)
    #             payment_term_id = self.env['account.payment.term'].search([('name', '=', payment_terms)], limit=1)
    #             account_analytic_id = self.env['account.analytic.account'].search([('name', '=', order_lines_analytic_account), '|', ('active', '=', True), ('active', '=', False)], limit=1)
    #             analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', order_lines_analytic_tags)])
    #             # analytic_tag =False
    #             # if order_lines_analytic_tags:
    #             #     analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', order_lines_analytic_tags)])
    #             #     analytic_tag = [(6, 0, analytic_tag_ids.ids)]
    #             product_uom_id = self.env['uom.uom'].search([('name', '=', order_lines_unit_of_measure)], limit=1)
    #
    #             search_purchase_order = self.env['purchase.order'].search([('name', '=', order_reference)])
    #
    #             lst = []
    #             if order_reference:
    #                 if order_lines_product:
    #                     po_line_vals = (0, 0, {
    #                         'product_id': pro_id.id,
    #                         'name': order_lines_description,
    #                         'date_planned': order_lines_scheduled_date,
    #                         'account_analytic_id': account_analytic_id.id,
    #                         'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
    #                         'product_qty': order_lines_quantity,
    #                         'product_uom': product_uom_id.id,
    #                         'price_unit': order_lines_price_unit,
    #                         'taxes_id': [(6, 0, tax_id.ids)],
    #                         # 'order_id': po_id.id
    #                     })
    #                     lst.append(po_line_vals)
    #
    #                 po_order_val = {
    #                     'name': order_reference,
    #                     'partner_id': part_id.id,
    #                     'partner_ref': vendor_reference,
    #                     'currency_id': c_id.id,
    #                     'date_order': order_date,
    #                     'date_planned': scheduled_date,
    #                     'user_id': use_id.id,
    #                     'invoice_status': billing_status,
    #                     'company_id': com_id.id,
    #                     'picking_type_id': pick_type_id.id,
    #                     'fiscal_position_id': fis_pos_id.id,
    #                     'state': status,
    #                     'date_approve': approval_date,
    #                     'incoterm_id': incoterm_id.id,
    #                     'payment_term_id': payment_term_id.id,
    #                     'order_line': lst,
    #                 }
    #                 if not search_purchase_order:
    #                     po_id = self.env['purchase.order'].create(po_order_val)
    #                     print(po_id)
    #             else:
    #                 po_line_vals = (0, 0, {
    #                     'product_id': pro_id.id,
    #                     'name': order_lines_description,
    #                     'date_planned': order_lines_scheduled_date,
    #                     'account_analytic_id': account_analytic_id.id,
    #                     'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
    #                     'product_qty': order_lines_quantity,
    #                     'product_uom': product_uom_id.id,
    #                     'price_unit': order_lines_price_unit,
    #                     'taxes_id': [(6, 0, tax_id.ids)],
    #                     # 'order_id': po_id.id
    #                 })
    #                 if po_id:
    #                     lst.append(po_line_vals)
    #                     po_line_id = po_id.write({'order_line': lst})
    #                     print(po_line_id)
    #
