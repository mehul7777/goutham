from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class TimesheetWizard(models.TransientModel):
    _name = "timesheet.wizard"
    _description = "Timesheet Wizard"

    load_file = fields.Binary("Load File")

    def import_timesheet_data(self):
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
                date = value[1]
                employee = value[2]
                employee_custom_id = value[3]
                project = value[4]
                project_custom_id = value[5]
                task = value[6]
                task_custom_id = value[7]
                description = value[8]
                quantity = value[9]
                company = value[10]
                analytic_account = value[11]

                employee_id = self.env['hr.employee'].search([('name', '=', employee), ('custom_id', '=', employee_custom_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                project_id = self.env['project.project'].search([('name', '=', project), ('custom_id', '=', project_custom_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                task_id = self.env['project.task'].search([('name', '=', task),('custom_task_id', '=', task_custom_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                account_id = self.env['account.analytic.account'].search([('name', '=', analytic_account), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                company_id = self.env['res.company'].search([('name', '=', company)], limit=1)

                timesheet_val = {
                    'custom_timesheet_id': id,
                    'date': date,
                    'employee_id': employee_id.id,
                    'project_id': project_id.id,
                    'task_id': task_id.id,
                    'name': description,
                    'unit_amount': quantity,
                    'company_id': company_id.id,
                    'account_id': account_id.id,
                }
                timesheet_id = self.env['account.analytic.line'].sudo().create(timesheet_val)