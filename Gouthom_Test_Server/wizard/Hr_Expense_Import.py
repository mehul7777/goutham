from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging
import time

_logger = logging.getLogger(__name__)


class HrExpenseWizard(models.TransientModel):
    _name = "hr.expense.wizard"
    _description = "Hr Expense Wizard"

    load_file = fields.Binary("Load File")

    def import_expense_data(self):
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
            if key == 0:
                header_list.append(value)
            else:
                # print(value)
                id = value[0]
                description = value[1]
                product_name = value[2]
                product_internal_reference = value[3]
                vendor_name = value[4]
                vendor_custom_id = value[5]
                unit_price = value[6]
                quantity = value[7]
                unit_of_measure = value[8]
                taxes = value[9]
                bill_reference = value[10]
                date = value[11]
                account_name = value[12]
                employee = value[13]
                employee_custom_id = value[14]
                sale_order_lead_opportunity = value[15]
                sales_order = value[16]
                sales_order_custom_id = value[17]
                currency = value[18]
                analytic_account = value[19]
                analytic_tags = value[20]
                company = value[21]
                total = value[22]
                paid_by = value[23]
                status = value[24]

                product_id = self.env['product.product'].search(
                    [('name', '=', product_name), ('default_code', '=', product_internal_reference), '|',
                     ('active', '=', True), ('active', '=', False)],
                    limit=1)
                vendor_id = self.env['res.partner'].search(
                    [('name', '=', vendor_name), ('id_custom', '=', vendor_custom_id), '|',
                     ('active', '=', True), ('active', '=', False)],
                    limit=1)
                product_uom_id = self.env['uom.uom'].search([('name', '=', unit_of_measure)], limit=1)
                tax_id = self.env["account.tax"].search([('name', '=', taxes)], limit=1)
                account_id = self.env["account.account"].search([('name', '=', account_name)], limit=1)
                employee_id = self.env['hr.employee'].search(
                    [('name', '=', employee), ('custom_id', '=', employee_custom_id),
                     '|', ('active', '=', True), ('active', '=', False)], limit=1)
                sales_opportunity_id = self.env['crm.lead'].search([('name', '=', sale_order_lead_opportunity)],
                                                                   limit=1)
                sale_order_id = self.env['sale.order'].search(
                    [('name', '=', sales_order), ('custom_so_id', '=', sales_order_custom_id)], limit=1)
                currency_id = self.env['res.currency'].search([('name', '=', currency)], limit=1)
                account_analytic_id = self.env['account.analytic.account'].search(
                    [('name', '=', analytic_account), '|', ('active', '=', True), ('active', '=', False)],
                    limit=1)
                analytic_tags_ids = self.env["account.analytic.tag"].search([('name', '=', analytic_tags)],
                                                                            limit=1)
                company_id = self.env["res.company"].search([('name', '=', company)], limit=1)

                search_hr_expense = self.env["hr.expense"].search([('custom_expense_id', '=', id)])

                expense_vals = {
                    'custom_expense_id': id,
                    'name': description,
                    'product_id': product_id.id,
                    'vendor_id': vendor_id.id,
                    'unit_amount': unit_price,
                    'quantity': quantity,
                    'product_uom_id': product_uom_id.id,
                    'tax_ids': [(6, 0, tax_id.ids)],
                    'reference': bill_reference,
                    'date': date,
                    'account_id': account_id.id,
                    'employee_id': employee_id.id,
                    'sales_opportunity_id': sales_opportunity_id.id,
                    'sale_order_id': sale_order_id.id,
                    'currency_id': currency_id.id,
                    'analytic_account_id': account_analytic_id.id,
                    'analytic_tag_ids': [(6, 0, analytic_tags_ids.ids)],
                    'company_id': company_id.id,
                    'total_amount': total,
                    'payment_mode': paid_by,
                }
                if not search_hr_expense:
                    self.env['hr.expense'].create(expense_vals)
                else:
                    search_hr_expense.write(expense_vals)

    def create_report_for_expense(self):
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
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                expense_id = value[0]
                expense_report_status = value[1].strip()

                search_hr_expense = self.env["hr.expense"].search([('custom_expense_id', '=', expense_id)])

                if search_hr_expense:
                    if expense_report_status == "draft":
                        search_hr_expense.write({'state': expense_report_status})
                    elif expense_report_status == "reported":
                        search_hr_expense.action_submit_expenses()
                    elif expense_report_status == "approve":
                        sheet = search_hr_expense.action_submit_expenses()
                        if sheet:
                            sheet_id = sheet['res_id']
                            if sheet_id:
                                sheet_record_id = self.env['hr.expense.sheet'].browse(sheet_id)
                                if sheet_record_id:
                                    # time.sleep(2)
                                    search_hr_expense.action_view_sheet()
                                    # time.sleep(2)
                                    sheet_record_id.approve_expense_sheets()
                    elif expense_report_status == "post" or "done":
                        sheet = search_hr_expense.action_submit_expenses()
                        if sheet:
                            sheet_id = sheet['res_id']
                            if sheet_id:
                                sheet_record_id = self.env['hr.expense.sheet'].browse(sheet_id)
                                if sheet_record_id:
                                    # time.sleep(2)
                                    search_hr_expense.action_view_sheet()
                                    # time.sleep(2)
                                    sheet_record_id.approve_expense_sheets()
                                    # time.sleep(2)
                                    sheet_record_id.action_sheet_move_create()
