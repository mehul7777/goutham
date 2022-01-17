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
                type = value[0]
                number = value[1]
                partner = value[2]
                payment_ref = value[3]
                invoice_date = value[4]
                due_date = value[5]
                currency = value[6]
                invoice_lines_product = value[7]
                invoice_lines_description = value[8]
                invoice_lines_asset_category = value[9]
                invoice_lines_account = value[10]
                invoice_lines_analytic_account = value[11]
                invoice_lines_analytic_tags = value[12]
                invoice_lines_category = value[13]
                invoice_lines_quantity = value[14]
                invoice_lines_unit_of_measure = value[15]
                invoice_lines_unit_price = value[16]
                invoice_lines_discount = value[17]
                invoice_lines_taxes = value[18]
                journal = value[19]
                account = value[20]
                accounting_date = value[21]
                reference_or_description = value[22]
                incoterm = value[23]
                fiscal_position = value[24]
                payment_terms = value[25]
                journal_entry = value[26]
                company = value[27]
                status = value[28]

                # For main class
                partner_id = self.env["res.partner"].search([('name', '=', partner), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                currency_id = self.env["res.currency"].search([('name', '=', currency)], limit=1)
                journal_id = self.env["account.journal"].search([('name', '=', journal)], limit=1)
                account_id = self.env["account.account"].search([('name', '=', account)], limit=1)
                invoice_incoterm_id = self.env["account.incoterms"].search([('name', '=', incoterm)], limit=1)
                fiscal_position_id = self.env["account.fiscal.position"].search([('name', '=', fiscal_position)], limit=1)
                invoice_payment_term_id = self.env["account.payment.term"].search([('name', '=', payment_terms)], limit=1)
                journal_entry_id = self.env["account.move"].search([('name', '=', journal_entry)], limit=1)
                company_id = self.env["res.company"].search([('name', '=', company)], limit=1)

                # For one2many
                product_id = self.env["product.product"].search([('name', '=', invoice_lines_product)], limit=1)
                asset_category_id = self.env["account.asset.category"].search([('name', '=', invoice_lines_asset_category)], limit=1)
                account_id = self.env["account.account"].search([('name', '=', invoice_lines_account)], limit=1)
                analytic_account_id = self.env['account.analytic.account'].search(
                    [('name', '=', invoice_lines_analytic_account), '|', ('active', '=', True), ('active', '=', False)],
                    limit=1)
                analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', invoice_lines_analytic_tags)],
                                                                           limit=1)
                product_uom_id = self.env['uom.uom'].search([('name', '=', invoice_lines_unit_of_measure)], limit=1)
                tax_ids = self.env['account.tax'].search([('name', '=', invoice_lines_taxes)], limit=1)

                lst = []
                if type:
                    if invoice_lines_product:
                        vendor_bill_line_vals = (0, 0, {
                            'product_id': product_id.id,
                            'name': invoice_lines_description,
                            'asset_category_id': asset_category_id.id,
                            'account_id': account_id.id,
                            'analytic_account_id': analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                            'invoice_lines_category': invoice_lines_category, # create this field
                            'quantity': invoice_lines_quantity,
                            'product_uom_id': product_uom_id.id,
                            'price_unit': invoice_lines_unit_price,
                            'discount': invoice_lines_discount,
                            'tax_ids': [(6, 0, tax_ids.ids)],
                        })

                        lst.append(vendor_bill_line_vals)

                    vendor_bill_vals = {
                        'move_type': type,
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
                        'state': "draft",
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
                            'account_id': account_id.id,
                            'analytic_account_id': analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                            'invoice_lines_category': invoice_lines_category, # create this field
                            'quantity': invoice_lines_quantity,
                            'product_uom_id': product_uom_id.id,
                            'price_unit': invoice_lines_unit_price,
                            'discount': invoice_lines_discount,
                            'tax_ids': [(6, 0, tax_ids.ids)],
                        })
                        lst.append(vendor_bill_line_vals)
                        vb_line_id = vb_id.write({'invoice_line_ids': lst})
                        print(vb_line_id)