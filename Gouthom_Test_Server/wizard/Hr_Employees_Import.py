from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class HrEmployeeWizard(models.TransientModel):
    _name = "hr.employee.wizard"
    _description = "Hr Employee Wizard"

    load_file = fields.Binary("Load File")

    def import_employee_data(self):
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
                name = value[0]
                tags = value[1]
                work_address = value[2]
                work_location = value[3]
                work_email = value[4]
                work_mobile = value[5]
                work_phone = value[6]
                id = value[7]
                department = value[8]
                job_position = value[9]
                job_title = value[10]
                manager = value[11]
                coach = value[12]
                is_a_manager = value[13]
                working_hours = value[14]
                timezone = value[15]
                nationality = value[16]
                ssn = value[17]
                passport_no = value[18]
                bank_account_number = value[19]
                private_address = value[20]
                emergency_contact = value[21]
                emergency_phone = value[22]
                km_home_work = value[23]
                gender = value[24]
                marital_status = value[25]
                number_of_children = value[26]
                date_of_birth = value[27] or False
                place_of_birth = value[28] or False
                country_birth = value[29] or False
                visa_no = value[30]
                work_permit_no = value[31]
                visa_expire_date = value[32] or False
                certificate_level = value[33]
                field_of_study = value[34]
                school = value[35]
                employee_documents = value[36]
                additional_note = value[37]
                timesheet_cost = value[38]
                timesheet_validation_date = value[39] or False
                timesheet_responsible = value[40]
                expense_responsible = value[41]
                company = value[42]
                responsible_user = value[43]
                remaining_legal_leaves = value[44]
                medical_examination_date = value[45] or False
                company_vehicle = value[46]
                badge_id = value[47]
                manual_attendance = value[48]
                job_description = value[49]
                active = value[50]

                category_ids = self.env['hr.employee.category'].search([('name', '=', tags)], limit=1)
                address_id = self.env['res.partner'].search([('name', '=', work_address), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                department_id = self.env['hr.department'].search([('name', '=', department), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                job_id = self.env['hr.job'].search([('name', '=', job_position)], limit=1)
                parent_id = self.env['hr.employee'].search([('name', '=', manager), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                coach_id = self.env['hr.employee'].search([('name', '=', coach), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                resource_calendar_id = self.env['resource.calendar'].search([('name', '=', working_hours), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                country_id = self.env['res.country'].search([('name', '=', nationality)], limit=1)
                # bank_account_id = self.env['res.partner.bank'].search([('name', '=', bank_account_number), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                address_home_id = self.env['res.partner'].search([('name', '=', private_address), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                country_of_birth = self.env['res.country'].search([('name', '=', country_birth)], limit=1)
                company_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                activity_user_id = self.env['res.users'].search([('name', '=', responsible_user), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                timesheet_responsible_id = self.env['res.users'].search([('name', '=', timesheet_responsible), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                expense_responsible_id = self.env['res.users'].search([('name', '=', expense_responsible), '|', ('active', '=', True), ('active', '=', False)], limit=1)

                if not department_id:
                    department_val = {
                        'name': department
                    }
                    department_id = self.env['hr.department'].create(department_val)

                if not job_id:
                    job_position_val = {
                        'name': job_position
                    }
                    job_id = self.env['hr.department'].create(job_position_val)

                if name:
                    employee_val = {
                        'name': name,
                        'category_ids': [(6, 0, category_ids.ids)],
                        'address_id': address_id.id,
                        'work_location': work_location,
                        'work_email': work_email,
                        'mobile_phone': work_mobile,
                        'work_phone': work_phone,
                        'custom_id': id,
                        'department_id': department_id.id,
                        # 'job_id': job_id.id,
                        'job_title': job_title,
                        'parent_id': parent_id.id,
                        'coach_id': coach_id.id,
                        'is_a_manager': is_a_manager,
                        'resource_calendar_id': resource_calendar_id.id,
                        'tz': timezone,
                        'country_id': country_id.id,
                        'ssnid': ssn,
                        'passport_id': passport_no,
                        # 'bank_account_id': bank_account_id.id,
                        'address_home_id': address_home_id.id,
                        'emergency_contact': emergency_contact,
                        'emergency_phone': emergency_phone,
                        'km_home_work': km_home_work,
                        'gender': gender,
                        'marital': marital_status,
                        'children': number_of_children,
                        'birthday': date_of_birth,
                        'place_of_birth': place_of_birth,
                        'country_of_birth': country_of_birth.id,
                        'visa_no': visa_no,
                        'permit_no': work_permit_no,
                        'visa_expire': visa_expire_date,
                        'certificate': certificate_level,
                        'study_field': field_of_study,
                        'study_school': school,
                        'additional_note': additional_note,
                        'timesheet_cost': timesheet_cost,
                        'timesheet_validation_date': timesheet_validation_date,
                        'timesheet_responsible_id': timesheet_responsible_id.id,
                        'expense_responsible_id': expense_responsible_id.id,
                        'company_id': company_id.id,
                        'activity_user_id': activity_user_id.id,
                        'remaining_legal_leaves': remaining_legal_leaves,
                        'medical_examination_date': medical_examination_date,
                        # 'vehicle': company_vehicle,
                        'barcode': badge_id,
                        'manual_attendance': manual_attendance,
                        'job_description': job_description,
                        'active': active
                    }
                    employee_id = self.env['hr.employee'].sudo().create(employee_val)