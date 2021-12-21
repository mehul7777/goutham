from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class ProjectWizard(models.TransientModel):
    _name = "project.wizard"
    _description = "Project Wizard"

    load_file = fields.Binary("Load File")

    def import_project_data(self):
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
                name = value[0]
                use_tasks_as = value[1]
                allow_timesheets = value[2]
                allow_forecast = value[3]
                project_manager = value[4]
                id = value[5]
                project_type = value[6]
                created_by = value[7]
                start_date = value[8]
                expiration_date = value[9]
                privacy = value[10]
                customer = value[11]
                analytic_account = value[12]
                sub_task_project = value[13]
                sequence = value[14]
                company = value[15]
                working_time = value[16]
                alias_name = value[17]
                alias_contact_name = value[18]
                sales_order = value[19]

                user_id = self.env['res.users'].search([('name', '=', project_manager), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                custom_created_by_id = self.env['res.users'].search([('name', '=', created_by), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                partner_id = self.env['res.partner'].search([('name', '=', customer)], limit=1)
                analytic_account_id = self.env['account.analytic.account'].search([('name', '=', analytic_account), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                subtask_project_id = self.env['project.project'].search([('name', '=', sub_task_project)], limit=1)
                company_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                resource_calendar_id = self.env['resource.calendar'].search([('name', '=', working_time)], limit=1)
                sale_order_id = self.env['sale.order'].search([('name', '=', sales_order)], limit=1)

                if not resource_calendar_id:
                    resource_calendar_id_val = {
                        'name': working_time
                    }
                    resource_calendar_id = self.env['resource.calendar'].create(resource_calendar_id_val)

                if name:
                    projects_val = {
                        'name': name,
                        'label_tasks': use_tasks_as,
                        'allow_timesheets': True if allow_timesheets == "True" else False,
                        'allow_forecast': True if allow_forecast == "True" else False,
                        'user_id': user_id.id,
                        'custom_id': id,
                        'project_type': project_type,
                        'custom_created_by': custom_created_by_id.id,
                        'date_start': start_date,
                        'date': expiration_date,
                        'privacy_visibility': privacy,
                        'partner_id': partner_id.id,
                        'analytic_account_id': analytic_account_id.id,
                        'subtask_project_id': subtask_project_id.id,
                        'sequence': sequence,
                        'company_id': company_id.id,
                        'resource_calendar_id': resource_calendar_id.id,
                        'alias_name': alias_name,
                        'alias_contact': alias_contact_name,
                        'sale_order_id': sale_order_id.id,
                    }
                    project_obj_id = self.env['project.project'].create(projects_val)
                    print("projects_val", project_obj_id)