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

                part_id = self.env['res.partner'].search([('name', '=', partner)], limit=1)
                jour_id = self.env['account.journal'].search([('name', '=', journal)])
                ino_use_id = self.env['res.users'].search([('name', '=', sales_person)])
                tea_id = self.env['crm.team'].search([('name', '=', sales_team)])
                cur_id = self.env['res.currency'].search([('name', '=', currency)])
                com_id = self.env['res.company'].search([('name', '=', company)])
                fis_pos_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position)])
                invoice_payment_term_id = self.env['account.payment.term'].search([('name', '=', payment_terms)])

                pro_id = self.env['product.product'].search([('name', '=', invoice_lines_product)], limit=1)
                acc_id = self.env['account.account'].search([('code', '=', invoice_lines_account)])
                ana_acc_id = self.env['account.analytic.account'].search(
                    [('name', '=', invoice_lines_analytic_account)], limit=1)
                analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', invoice_lines_analytic_tags)])
                pro_uom_id = self.env['uom.uom'].search([('name', '=', invoice_lines_unit_of_measure)])
                tax_ids = self.env['account.tax'].search([('name', '=', invoice_lines_taxes)], limit=1)

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

                    if tax_lines_tax_account:
                        tax_lines_val = (0, 0, {
                            '': tax_lines_description,
                            '': tax_lines_tax_account,
                            '': tax_lines_analytic_account,
                            '': tax_lines_analytic_tags,
                        })

                    ci_val = {
                        'move_type': type,
                        'name': number,
                        'partner_id': part_id.id,
                        'partner_shipping_id': delivery_address,
                        'invoice_payment_term_id': invoice_payment_term_id.id,
                        'payment_reference': payment_ref,
                        'customer_po': customer_po, # create this field
                        'point_of_contact': point_of_contact, # create this field
                        'point_of_contact_po': point_of_contact_po, # create this field
                        'invoice_date': invoice_date,
                        'invoice_date_due': due_date,
                        'journal_id': jour_id.id,
                        'ref': reference_description,
                        'project_manager': project_manager, # create this field
                        'account': account, # create this field
                        'incoterm': incoterm, # create this field
                        'journal_entry': journal_entry, # create this field
                        'source_document': source_document, # create this field
                        'invoice_user_id': ino_use_id.id,
                        'team_id': tea_id.id,
                        'currency_id': cur_id.id,
                        'company_id': com_id.id,
                        'fiscal_position_id': fis_pos_id.id,
                        'state': status,
                        'invoice_line_ids': lst,
                    }
                    ci_id = self.env['account.move'].create(ci_val)
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

