from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class ProjectTaskWizard(models.TransientModel):
    _name = "project.task.wizard"
    _description = "Project Task Wizard"

    load_file = fields.Binary("Load File")

    def import_task_data(self):
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
                title = value[0]
                project = value[1]
                assigned_to = value[2]
                starting_date = value[3] or False
                ending_date = value[4] or False
                sales_order_item = value[5]
                tags = value[6]
                deadline = value[7] or False
                created_on = value[8]
                sequence = value[9]
                customer = value[10]
                customer_id = value[11]
                email = value[12]
                watchers_emails = value[13]
                parent_task = value[14]
                company = value[15]
                cover_image = value[16]
                assigning_date = value[17] or False
                last_stage_update = value[18] or False
                stage = value[19]
                active = value[20]

                project_id = self.env['project.project'].search([('name', '=', project), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                user_id = self.env['res.users'].search([('name', '=', assigned_to), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                sale_line_id = self.env['sale.order.line'].search([('name', '=', sales_order_item)], limit=1)
                tag_ids = self.env['project.tags'].search([('name', '=', tags)], limit=1)
                partner_id = self.env['res.partner'].search([('name', '=', customer), ('id_custom', '=', customer_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                parent_id = self.env['project.task'].search([('name', '=', parent_task)], limit=1)
                company_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                displayed_image_id = self.env['ir.attachment'].search([('name', '=', cover_image)], limit=1)
                stage_id = self.env['project.task.type'].search([('name', '=', stage)], limit=1)

                if title:
                    tasks_val = {
                        'name': title,
                        'project_id': project_id.id,
                        'user_id': user_id.id,
                        'starting_date': starting_date,
                        'date_end': ending_date,
                        'sale_line_id': sale_line_id.id,
                        'tag_ids': [(6, 0, tag_ids.ids)],
                        'date_deadline': deadline,
                        'create_date': created_on,
                        'custom_create_date': created_on,
                        'sequence': sequence,
                        'partner_id': partner_id.id,
                        'email_from': email,
                        'email_cc': watchers_emails,
                        'parent_id': parent_id.id,
                        'company_id': company_id.id,
                        'displayed_image_id': displayed_image_id.id,
                        # 'date_assign': assigning_date,
                        # 'date_last_stage_update': last_stage_update,
                        'stage_id': stage_id.id,
                        'active': True if active == "True" else False,
                    }
                    task_obj_id = self.env['project.task'].sudo().create(tasks_val)
                    dates_val = {
                        'date_assign': assigning_date,
                        'date_last_stage_update': last_stage_update,
                    }
                    task_obj_id.write(dates_val)
                    print("tasks_val", task_obj_id)