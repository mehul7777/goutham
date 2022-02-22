import time
from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging
import json
from odoo.tools import float_compare, date_utils, email_split, email_re

_logger = logging.getLogger(__name__)


class CustomerInvoiceWizard(models.TransientModel):
    _name = "customer.invoice.wizard"
    _description = "Customer Invoice Wizard"

    load_file = fields.Binary("Load File")

    def post_draft_invoice(self):
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
                status = value[1]

                search_cust_invoice = self.env["account.move"].search(
                    [('move_type', '=', 'out_invoice'), ('custom_id', '=', id),
                     ('state', '=', 'draft'), ('payment_state', '=', 'not_paid')])

                if search_cust_invoice:
                    if status == "paid":
                        search_cust_invoice.action_post()
                    else:
                        search_cust_invoice.write({'state': status})

    def paid_post_invoice(self):
        # print("Import is working for create payment")
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
                # print(value)
                number = value[0]
                payments_widget = value[1]
                total = value[2]

                # print(payments_widget)

                payments_widget_dict = json.loads(payments_widget)
                print(payments_widget_dict['content'])

                search_cust_invoice = self.env["account.move"].search(
                    [('name', '=', number), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                     ('payment_state', '=', 'not_paid')])

                print(search_cust_invoice)

                for payment_values in payments_widget_dict['content']:
                    # print("\n")
                    # print(payment_values['journal_name'])
                    # print(payment_values['amount'])
                    # print(payment_values['date'])
                    # print(payment_values['ref'])

                    journal_id = self.env["account.journal"].search([('name', '=', payment_values['journal_name'])])
                    # journal_id_stripe = self.env['account.journal'].sudo().search([('code', '=', 'BANK')], limit=1).id
                    if search_cust_invoice:
                        payment_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                       active_ids=search_cust_invoice.ids).create(
                            {
                                'journal_id': journal_id.id,
                                'amount': payment_values['amount'],
                                'company_id': search_cust_invoice.company_id.id,
                                'currency_id': search_cust_invoice.currency_id.id,
                                'partner_id': search_cust_invoice.partner_id.id,
                                'partner_type': 'customer',
                                'payment_date': payment_values['date'],
                                'payment_type': 'inbound',
                                # 'payment_method_code': "CASH" if payment_values['ref'][0]=="C" else "BANK",
                            })
                        account_payment = payment_wizard._create_payments()
                        account_payment.write({'custom_number': payment_values['ref']})

                """"# payment_vals = {
                #     'amount': amount,
                #     # 'communication': search_cust_invoice.payment_reference,
                #     'company_id': search_cust_invoice.company_id.id,
                #     'currency_id': search_cust_invoice.currency_id.id,
                #     'journal_id': journal_id.id,
                #     'line_ids': [(6, 0, i.ids)],
                #     # 'partner_bank_id': ,
                #     'partner_type': 'customer',
                #     'date': payment_date,
                #     # 'payment_method_id': ,
                #     'payment_type': 'inbound',
                #     'custom_number': ref,
                #     # 'payment_difference_handling': 'reconcile',
                # }"""

    def import_customer_invoice_data(self):
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
        ci_id = ''
        for key, value in data_dict.items():
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                id = value[0]
                type = value[1]
                number = value[2]
                partner = value[3]
                partner_custom_id = value[4]
                delivery_address = value[5]
                payment_terms = value[6]
                reference_description = value[7]
                customer_po = value[8]
                invoice_date = value[9] or False
                due_date = value[10] or False
                sales_person = value[11]
                project_manager = value[12]
                sales_team = value[13]
                currency = value[14]
                point_of_contact = value[15]
                point_of_contact_po = value[16]
                invoice_lines_display_type = value[17]
                invoice_lines_product = value[18]
                invoice_lines_product_internal_reference = value[19]
                invoice_lines_description = value[20]
                invoice_lines_account = value[21]
                invoice_lines_analytic_account = value[22]
                invoice_lines_analytic_tags = value[23]
                invoice_lines_quantity = value[24]
                invoice_lines_unit_of_measure = value[25]
                invoice_lines_unit_price = value[26]
                invoice_lines_discount = value[27]
                invoice_lines_taxes = value[28]
                journal = value[29]
                account = value[30]
                company = value[31]
                payment_ref = value[32]
                incoterm = value[33]
                fiscal_position = value[34]
                journal_entry = value[35]
                source_document = value[36]

                if not invoice_lines_product and invoice_lines_unit_of_measure:
                    invoice_lines_product = 'Service'
                    invoice_lines_product_internal_reference = 'Service'

                if not invoice_lines_analytic_account:
                    invoice_lines_analytic_account = 'NOT DEFINE'

                part_id = self.env['res.partner'].search(
                    [('name', '=', partner),('id_custom', '=', partner_custom_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                jour_id = self.env['account.journal'].search([('name', '=', journal)], limit=1)
                ino_use_id = self.env['res.users'].search(
                    [('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                tea_id = self.env['crm.team'].search(
                    [('name', '=', sales_team), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                cur_id = self.env['res.currency'].search([('name', '=', currency)], limit=1)
                com_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                fis_pos_id = self.env['account.fiscal.position'].search(
                    [('name', '=', fiscal_position), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                invoice_payment_term_id = self.env['account.payment.term'].search([('name', '=', payment_terms)],
                                                                                  limit=1)
                invoice_incoterm_id = self.env['account.incoterms'].search([('name', '=', incoterm)], limit=1)
                point_of_contact_id = self.env['res.partner'].search(
                    [('name', '=', point_of_contact), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                project_manager_id = self.env['res.users'].search(
                    [('name', '=', project_manager), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                account_id = self.env['account.account'].search([('name', '=', account)], limit=1)
                journal_entry_id = self.env['account.move'].search([('name', '=', journal_entry)], limit=1)
                partner_shipping_id = self.env['res.partner'].search(
                    [('name', '=', delivery_address), '|', ('active', '=', True), ('active', '=', False)], limit=1)

                pro_id = self.env['product.product'].search(
                    ['|', ('name', '=', invoice_lines_product), ('default_code', '=', invoice_lines_product_internal_reference),'|', ('active', '=', True), ('active', '=', False)], limit=1)
                acc_id = self.env['account.account'].search([('name', '=', invoice_lines_account)], limit=1)
                ana_acc_id = self.env['account.analytic.account'].search(
                    [('name', '=', invoice_lines_analytic_account), '|', ('active', '=', True), ('active', '=', False)],
                    limit=1)
                analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', invoice_lines_analytic_tags)],
                                                                           limit=1)
                pro_uom_id = self.env['uom.uom'].search([('name', '=', invoice_lines_unit_of_measure)], limit=1)
                tax_ids = self.env['account.tax'].search([('name', '=', invoice_lines_taxes)], limit=1)

                lst = []
                if type:
                    if not invoice_lines_unit_of_measure:
                        vals = (0, 0, {
                            'display_type': invoice_lines_display_type,
                            'name': invoice_lines_description,
                        })

                        lst.append(vals)
                    if invoice_lines_product:
                        vals = (0, 0, {
                            'product_id': pro_id.id,
                            'name': invoice_lines_description,
                            'account_id': acc_id.id,
                            'analytic_account_id': ana_acc_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                            'quantity': invoice_lines_quantity,
                            'product_uom_id': pro_uom_id.id,
                            'price_unit': invoice_lines_unit_price,
                            'discount': invoice_lines_discount,
                            'tax_ids': [(6, 0, tax_ids.ids)],
                        })

                        lst.append(vals)

                    ci_val = {
                        'custom_id': id,
                        'move_type': type,
                        'name': number,
                        'partner_id': part_id.id,
                        'partner_shipping_id': partner_shipping_id.id,
                        'invoice_payment_term_id': invoice_payment_term_id.id,
                        'payment_reference': payment_ref,
                        'customer_po': customer_po,
                        'point_of_contact_id': point_of_contact_id.id,
                        'point_of_contact_po': point_of_contact_po,
                        'invoice_date': invoice_date,
                        'invoice_date_due': due_date,
                        'journal_id': jour_id.id,
                        'ref': reference_description,
                        'project_manager_id': project_manager_id.id,
                        'account_id': account_id.id,
                        'invoice_incoterm_id': invoice_incoterm_id.id,
                        'journal_entry_id': journal_entry_id.id,
                        'source_document': source_document,
                        'invoice_user_id': ino_use_id.id,
                        'team_id': tea_id.id,
                        'currency_id': cur_id.id,
                        'company_id': com_id.id,
                        'fiscal_position_id': fis_pos_id.id,
                        'invoice_line_ids': lst,
                    }
                    ci_id = self.env['account.move'].sudo().create(ci_val)
                    print("ci_val", ci_val)
                else:
                    if not invoice_lines_unit_of_measure:
                        vals = (0, 0, {
                            'display_type': invoice_lines_display_type,
                            'name': invoice_lines_description,
                        })

                        lst.append(vals)
                        ci_line_id = ci_id.write({'invoice_line_ids': lst})
                        print(ci_line_id)
                    if invoice_lines_product:
                        vals = (0, 0, {
                            'product_id': pro_id.id,
                            'name': invoice_lines_description,
                            'account_id': acc_id.id,
                            'analytic_account_id': ana_acc_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                            'quantity': invoice_lines_quantity,
                            'product_uom_id': pro_uom_id.id,
                            'price_unit': invoice_lines_unit_price,
                            'discount': invoice_lines_discount,
                            'tax_ids': [(6, 0, tax_ids.ids)],
                        })
                        lst.append(vals)
                        ci_line_id = ci_id.write({'invoice_line_ids': lst})
                        print(ci_line_id)