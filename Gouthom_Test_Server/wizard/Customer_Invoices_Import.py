from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class CustomerInvoiceWizard(models.TransientModel):
    _name = "customer.invoice.wizard"
    _description = "Customer Invoice Wizard"

    load_file = fields.Binary("Load File")

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
                type = value[0]
                number = value[1]
                partner = value[2]
                delivery_address = value[3]
                payment_terms = value[4]
                reference_description = value[5]
                customer_po = value[6]
                invoice_date = value[7]
                due_date = value[8]
                sales_person = value[9]
                project_manager = value[10]
                sales_team = value[11]
                currency = value[12]
                point_of_contact = value[13]
                point_of_contact_po = value[14]
                invoice_lines_product = value[15]
                invoice_lines_description = value[16]
                invoice_lines_account = value[17]
                invoice_lines_analytic_account = value[18]
                invoice_lines_analytic_tags = value[19]
                invoice_lines_quantity = value[20]
                invoice_lines_unit_of_measure = value[21]
                invoice_lines_unit_price = value[22]
                invoice_lines_discount = value[23]
                invoice_lines_taxes = value[24]
                journal = value[25]
                account = value[26]
                company = value[27]
                payment_ref = value[28]
                incoterm = value[29]
                fiscal_position = value[30]
                journal_entry = value[31]
                source_document = value[32]
                tax_lines_description = value[33]
                tax_lines_tax_account = value[34]
                tax_lines_analytic_account = value[35]
                tax_lines_analytic_tags = value[36]
                status = value[37]

                part_id = self.env['res.partner'].search([('name', '=', partner), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                jour_id = self.env['account.journal'].search([('name', '=', journal)], limit=1)
                ino_use_id = self.env['res.users'].search([('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                tea_id = self.env['crm.team'].search([('name', '=', sales_team), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                cur_id = self.env['res.currency'].search([('name', '=', currency)], limit=1)
                com_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                fis_pos_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                invoice_payment_term_id = self.env['account.payment.term'].search([('name', '=', payment_terms)], limit=1)
                invoice_incoterm_id = self.env['account.incoterms'].search([('name', '=', incoterm)], limit=1)
                point_of_contact_id = self.env['res.partner'].search([('name', '=', point_of_contact), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                project_manager_id = self.env['res.users'].search([('name', '=', project_manager), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                account_id = self.env['account.account'].search([('name', '=', account)], limit=1)
                journal_entry_id = self.env['account.move'].search([('name', '=', journal_entry)], limit=1)
                partner_shipping_id = self.env['res.partner'].search([('name', '=', delivery_address), '|', ('active', '=', True), ('active', '=', False)], limit=1)

                pro_id = self.env['product.product'].search([('name', '=', invoice_lines_product), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                acc_id = self.env['account.account'].search([('name', '=', invoice_lines_account)], limit=1)
                ana_acc_id = self.env['account.analytic.account'].search([('name', '=', invoice_lines_analytic_account), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', invoice_lines_analytic_tags)], limit=1)
                pro_uom_id = self.env['uom.uom'].search([('name', '=', invoice_lines_unit_of_measure)], limit=1)
                tax_ids = self.env['account.tax'].search([('name', '=', invoice_lines_taxes)], limit=1)

                tax_account_id = self.env['account.account'].search([('name', '=', tax_lines_tax_account)], limit=1)
                tax_analytic_account_id = self.env['account.analytic.account'].search([('name', '=', tax_lines_analytic_account), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                tax_analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', tax_lines_analytic_tags)], limit=1)

                lst = []
                tax_lines_lst = []
                if type:
                    if invoice_lines_product:
                        vals = (0, 0, {
                            'product_id': pro_id.id,
                            'name': invoice_lines_description,
                            'account_id': acc_id.id,
                            'analytic_account_id': ana_acc_id.id,
                            'analytic_tag_ids':  [(6, 0, analytic_tag_ids.ids)],
                            'quantity': invoice_lines_quantity,
                            'product_uom_id': pro_uom_id.id,
                            'price_unit': invoice_lines_unit_price,
                            'discount': invoice_lines_discount,
                            'tax_ids': [(6, 0, tax_ids.ids)],
                        })

                        lst.append(vals)

                    # if tax_lines_tax_account:
                    #     tax_lines_val = (0, 0, {
                    #         'name': tax_lines_description,
                    #         'account_id': tax_account_id.id,
                    #         'analytic_account_id': tax_analytic_account_id.id,
                    #         'analytic_tag_ids': [(6, 0, tax_analytic_tag_ids.ids)],
                    #     })
                    #
                    #     tax_lines_lst.append(tax_lines_val)

                    ci_val = {
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
                        'state': status,
                        'invoice_line_ids': lst,
                        # 'line_ids': tax_lines_lst,
                    }
                    ci_id = self.env['account.move'].sudo().create(ci_val)
                    print("ci_val", ci_val)
                else:
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

                    # if tax_lines_tax_account:
                    #     tax_lines_val = (0, 0, {
                    #         'name': tax_lines_description,
                    #         'account_id': tax_account_id.id,
                    #         'analytic_account_id': tax_analytic_account_id.id,
                    #         'analytic_tag_ids': [(6, 0, tax_analytic_tag_ids.ids)],
                    #     })
                    #
                    #     tax_lines_lst.append(tax_lines_val)
                    #     ci_tax_line_id = ci_id.write({'line_ids': tax_lines_lst})