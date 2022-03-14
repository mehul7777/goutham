import json
from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class VendorBillWizard(models.TransientModel):
    _name = "vendor.bill.wizard"
    _description = "Vendor Bill Wizard"

    load_file = fields.Binary("Load File")

    def add_custom_numbers(self):
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
                id = value[0]
                number = value[1]

                search_vendor_bill = self.env["account.move"].search(
                    [('move_type', '=', 'in_invoice'), ('custom_id', '=', id)])

                if search_vendor_bill:
                    search_vendor_bill.write({'custom_number': number})

    def post_draft_bills(self):
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

                search_vendor_bill = self.env["account.move"].search(
                    [('move_type', '=', 'in_invoice'), ('custom_id', '=', id),
                     ('state', '=', 'draft'), ('payment_state', '=', 'not_paid')])

                if search_vendor_bill:
                    if status == "paid":
                        search_vendor_bill.action_post()
                    else:
                        search_vendor_bill.write({'state': status})

    def paid_post_bills(self):
        print("Import is working for vendor bill payment")
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
                payments_widget = value[1]

                payments_widget_dict = json.loads(payments_widget)

                search_vendor_bills = self.env["account.move"].search(
                    [('custom_id', '=', id), ('move_type', '=', 'in_invoice'), ('state', '=', 'posted'),
                     ('payment_state', '=', 'not_paid')])

                for payment_values in payments_widget_dict['content']:
                    journal_id = self.env["account.journal"].search([('name', '=', payment_values['journal_name'])])

                    if search_vendor_bills:
                        payment_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                       active_ids=search_vendor_bills.ids).create(
                            {
                                'journal_id': journal_id.id,
                                'amount': payment_values['amount'],
                                'company_id': search_vendor_bills.company_id.id,
                                'currency_id': search_vendor_bills.currency_id.id,
                                'partner_id': search_vendor_bills.partner_id.id,
                                'partner_type': 'supplier',
                                'payment_date': payment_values['date'],
                                'payment_type': 'outbound',
                            })
                        account_payment = payment_wizard._create_payments()
                        account_payment.write({'custom_number': payment_values['ref']})

    def import_vendor_bill_data(self):
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
        vb_id = ''
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
                payment_ref = value[5]
                source_document = value[6]
                invoice_date = value[7]
                due_date = value[8]
                currency = value[9]
                invoice_lines_product = value[10]
                invoice_lines_product_internal_reference = value[11]
                invoice_lines_description = value[12]
                invoice_lines_asset_category = value[13]
                invoice_lines_account = value[14]
                invoice_lines_analytic_account = value[15]
                invoice_lines_analytic_tags = value[16]
                invoice_lines_category = value[17]
                invoice_lines_quantity = value[18]
                invoice_lines_unit_of_measure = value[19]
                invoice_lines_unit_price = value[20]
                invoice_lines_discount = value[21]
                invoice_lines_taxes = value[22]
                purchase_representative = value[23]
                journal = value[24]
                account = value[25]
                accounting_date = value[26]
                reference_or_description = value[27]
                incoterm = value[28]
                fiscal_position = value[29]
                payment_terms = value[30]
                journal_entry = value[31]
                company = value[32]

                if not invoice_lines_product:
                    invoice_lines_product = 'Service'
                    invoice_lines_product_internal_reference = 'Service'

                if not invoice_lines_analytic_account:
                    invoice_lines_analytic_account = 'NOT DEFINE'

                # For main class
                partner_id = self.env["res.partner"].search([('name', '=', partner), ('id_custom', '=', partner_custom_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                currency_id = self.env["res.currency"].search([('name', '=', currency)], limit=1)
                journal_id = self.env["account.journal"].search([('name', '=', journal)], limit=1)
                account_id = self.env["account.account"].search([('name', '=', account)], limit=1)
                invoice_incoterm_id = self.env["account.incoterms"].search([('name', '=', incoterm)], limit=1)
                fiscal_position_id = self.env["account.fiscal.position"].search([('name', '=', fiscal_position)], limit=1)
                invoice_payment_term_id = self.env["account.payment.term"].search([('name', '=', payment_terms)], limit=1)
                journal_entry_id = self.env["account.move"].search([('name', '=', journal_entry)], limit=1)
                company_id = self.env["res.company"].search([('name', '=', company)], limit=1)

                # For one2many
                product_id = self.env["product.product"].search(["|", ('name', '=', invoice_lines_product),
                        ('default_code', '=', invoice_lines_product_internal_reference), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                asset_category_id = self.env["account.asset.category"].search([('name', '=', invoice_lines_asset_category)], limit=1)
                invoice_line_account_id = self.env["account.account"].search([('name', '=', invoice_lines_account)], limit=1)
                analytic_account_id = self.env['account.analytic.account'].search(
                    [('name', '=', invoice_lines_analytic_account), '|', ('active', '=', True), ('active', '=', False)],
                    limit=1)
                analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', invoice_lines_analytic_tags)],
                                                                           limit=1)
                product_uom_id = self.env['uom.uom'].search([('name', '=', invoice_lines_unit_of_measure)], limit=1)
                tax_ids = self.env['account.tax'].search([('name', '=', invoice_lines_taxes)], limit=1)
                purchase_representative_id = self.env['res.users'].search(
                    [('name', '=', purchase_representative), '|', ('active', '=', True), ('active', '=', False)],
                    limit=1)

                lst = []
                if type:
                    if invoice_lines_product:
                        vendor_bill_line_vals = (0, 0, {
                            'product_id': product_id.id,
                            'name': invoice_lines_description,
                            'asset_category_id': asset_category_id.id,
                            'account_id': invoice_line_account_id.id,
                            'analytic_account_id': analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                            'x_studio_category': invoice_lines_category,
                            'quantity': invoice_lines_quantity,
                            'product_uom_id': product_uom_id.id,
                            'price_unit': invoice_lines_unit_price,
                            'discount': invoice_lines_discount,
                            'tax_ids': [(6, 0, tax_ids.ids)],
                        })

                        lst.append(vendor_bill_line_vals)

                    vendor_bill_vals = {
                        'custom_id': id,
                        'move_type': type,
                        'custom_number': number,
                        'name': number,
                        'partner_id': partner_id.id,
                        'payment_reference': payment_ref,
                        'invoice_date': invoice_date,
                        'invoice_date_due': due_date,
                        'currency_id': currency_id.id,
                        'journal_id': journal_id.id,
                        'account_id': account_id.id,
                        'date': accounting_date,
                        'invoice_incoterm_id': invoice_incoterm_id.id,
                        'fiscal_position_id': fiscal_position_id.id,
                        'invoice_payment_term_id': invoice_payment_term_id.id,
                        'journal_entry_id': journal_entry_id.id,
                        'company_id': company_id.id,
                        'source_document': source_document,
                        'purchase_representative_id': purchase_representative_id.id,
                        'ref': reference_or_description,
                        'invoice_line_ids': lst,
                    }
                    vb_id = self.env['account.move'].sudo().create(vendor_bill_vals)
                    print("vendor_bill_vals", vendor_bill_vals)
                else:
                    if invoice_lines_product:
                        vendor_bill_line_vals = (0, 0, {
                            'product_id': product_id.id,
                            'name': invoice_lines_description,
                            'asset_category_id': asset_category_id.id,
                            'account_id': invoice_line_account_id.id,
                            'analytic_account_id': analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                            'x_studio_category': invoice_lines_category,
                            'quantity': invoice_lines_quantity,
                            'product_uom_id': product_uom_id.id,
                            'price_unit': invoice_lines_unit_price,
                            'discount': invoice_lines_discount,
                            'tax_ids': [(6, 0, tax_ids.ids)],
                        })
                        if vb_id:
                            lst.append(vendor_bill_line_vals)
                            vb_line_id = vb_id.write({'invoice_line_ids': lst})
                            print(vb_line_id)