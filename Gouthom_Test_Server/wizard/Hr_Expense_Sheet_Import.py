from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class HrExpenseSheetWizard(models.TransientModel):
    _name = "hr.expense.sheet.wizard"
    _description = "Hr Expense Sheet Wizard"

    load_file = fields.Binary("Load File")

    def import_expense_sheet_data(self):
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
        expense_sheet_id = ' '
        for key, value in data_dict.items():
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                id = value[0]
                expense_report_summery = value[1]
                employee = value[2]
                employee_custom_id = value[3]
                paid_by = value[4]
                manager = value[5]
                company = value[6]
                expense_line_date = value[7]
                expense_line_description = value[8]
                expense_line_account = value[9]
                expense_line_vendor = value[10]
                expense_line_vendor_id = value[11]
                expense_sale_order = value[12]
                expense_line_analytic_account = value[13]
                expense_line_analytic_tag = value[14]
                expense_line_attachment_count = value[15]
                expense_line_taxes = value[16]
                expense_line_total = value[17]
                expense_line_total_company_currency = value[18]
                expense_line_employee = value[19]
                expense_line_employee_id = value[20]
                expense_line_quantity = value[21]
                expense_line_unit_price = value[22]
                expense_line_unit_of_measure = value[23]
                expense_line_product = value[24]
                expense_line_product_internal_reference = value[25]
                created_on = value[26]
                bank_journal = value[27]
                status = value[28]
                date = value[29]

                employee_id = self.env['hr.employee'].search(
                    [('name', '=', employee), ('custom_id', '=', employee_custom_id), '|', ('active', '=', True),
                     ('active', '=', False)], limit=1)
                company_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                user_id = self.env['res.users'].search(
                    [('name', '=', manager), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                bank_journal_id = self.env['account.journal'].search([('name', '=', bank_journal)], limit=1)

                account_id = self.env['account.account'].search([('name', '=', expense_line_account)], limit=1)
                vendor_id = self.env['res.partner'].search(
                    [('name', '=', expense_line_vendor), ('id_custom', '=', expense_line_vendor_id), '|', ('active', '=', True),
                     ('active', '=', False)], limit=1)
                sale_order_id = self.env['sale.order'].search([('name', '=', expense_sale_order)], limit=1)
                analytic_account_id = self.env['account.analytic.account'].search(
                    [('name', '=', expense_line_analytic_account), '|', ('active', '=', True), ('active', '=', False)],
                    limit=1)
                analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', expense_line_analytic_tag)],
                                                                           limit=1)
                tax_ids = self.env['account.tax'].search([('name', '=', expense_line_taxes)], limit=1)
                product_uom_id = self.env['uom.uom'].search([('name', '=', expense_line_unit_of_measure)], limit=1)
                expense_employee_id = self.env['hr.employee'].search(
                    [('name', '=', expense_line_employee), ('custom_id', '=', expense_line_employee_id), '|', ('active', '=', True),
                     ('active', '=', False)], limit=1)
                product_id = self.env['product.product'].search(
                    ['|', ('name', '=', expense_line_product),
                     ('default_code', '=', expense_line_product_internal_reference), '|', ('active', '=', True),
                     ('active', '=', False)], limit=1)

                lst = []
                if id:
                    expense_sheet_line_vals = (0, 0, {
                        'employee_id': expense_employee_id.id,
                        'date': expense_line_date,
                        'name': expense_line_description,
                        'account_id': account_id.id,
                        'vendor_id': vendor_id.id,
                        'sale_order_id': sale_order_id.id,
                        'analytic_account_id': analytic_account_id.id,
                        'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                        'attachment_number': expense_line_attachment_count,
                        'tax_ids': [(6, 0, tax_ids.ids)],
                        'total_amount': expense_line_total,
                        'total_amount_company': expense_line_total_company_currency,
                        'quantity': expense_line_quantity,
                        'unit_amount': expense_line_unit_price,
                        'product_uom_id': product_uom_id.id,
                        'product_id': product_id.id
                    })

                    lst.append(expense_sheet_line_vals)

                    expense_sheet_vals = {
                        'custom_expense_sheet_id': id,
                        'name': expense_report_summery,
                        'employee_id': employee_id.id,
                        'payment_mode': paid_by,
                        'user_id': user_id.id,
                        'company_id': company_id.id,
                        'create_date': created_on,
                        'create_custom_date': created_on,
                        'bank_journal_id': bank_journal_id.id,
                        'state': status,
                        'accounting_date': date,
                        'expense_line_ids': lst
                    }
                    expense_sheet_id = self.env['hr.expense.sheet'].sudo().create(expense_sheet_vals)
                    expense_sheet_id.write({'create_date': created_on})
                else:
                    expense_sheet_line_vals = (0, 0, {
                        'employee_id': expense_employee_id.id,
                        'date': expense_line_date,
                        'name': expense_line_description,
                        'account_id': account_id.id,
                        'vendor_id': vendor_id.id,
                        'sale_order_id': sale_order_id.id,
                        'analytic_account_id': analytic_account_id.id,
                        'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                        'attachment_number': expense_line_attachment_count,
                        'tax_ids': [(6, 0, tax_ids.ids)],
                        'total_amount': expense_line_total,
                        'total_amount_company': expense_line_total_company_currency,
                        'quantity': expense_line_quantity,
                        'unit_amount': expense_line_unit_price,
                        'product_uom_id': product_uom_id.id,
                        'product_id': product_id.id
                    })
                    lst.append(expense_sheet_line_vals)
                    expense_sheet_line_id = expense_sheet_id.write({'expense_line_ids': lst})


