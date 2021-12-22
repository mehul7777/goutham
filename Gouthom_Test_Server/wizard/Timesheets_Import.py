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
                date = value[0]
                employee = value[1]
                project = value[2]
                task = value[3]
                description = value[4]
                quantity = value[5]

                employee_id = self.env['hr.employee'].search([('name', '=', employee), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                project_id = self.env['project.project'].search([('name', '=', project), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                task_id = self.env['project.task'].search([('name', '=', task), '|', ('active', '=', True), ('active', '=', False)], limit=1)

                timesheet_val = {
                    'date': date,
                    'employee_id': employee_id.id,
                    'project_id': project_id.id,
                    'task_id': task_id.id,
                    'name': description,
                    'unit_amount': quantity,
                }
                timesheet_id = self.env['account.analytic.line'].create(timesheet_val)