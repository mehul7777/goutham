from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class CRMWizard(models.TransientModel):
    _name = "crm.wizard"
    _description = "CRM Wizard"

    load_file = fields.Binary("Load File")

    def import_crm_data(self):
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
                opportunity = value[0]
                expected_revenue = value[1]
                probability = value[2]
                customer = value[3]
                email = value[4]
                phone = value[5]
                expected_closing = value[6] or False
                sales_person = value[7]
                sales_team = value[8]
                as_9100_from = value[9]
                priority = value[10]
                tags = value[11]
                customer_name = value[12]
                street = value[13]
                street2 = value[14]
                city = value[15]
                state = value[16]
                zip = value[17]
                country = value[18]
                website = value[19]
                contact_name = value[20]
                title = value[21]
                job_position = value[22]
                mobile = value[23]
                campaign = value[24]
                source = value[25]
                days_to_assign = str(value[26])
                days_to_close = str(value[27])
                referred_by = value[28]
                stage = value[29]

                partner_id = self.env['res.partner'].search([('name', '=', customer)])
                user_id = self.env['res.users'].search([('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)])
                team_id = self.env['crm.team'].search([('name', '=', sales_team)])
                tag_ids = self.env['crm.tag'].search([('name', '=', tags)])
                state_id = self.env['res.country.state'].search([('name', '=', state)])
                country_id = self.env['res.country'].search([('name', '=', country)])
                campaign_id = self.env['utm.campaign'].search([('name', '=', campaign)])
                source_id = self.env['utm.source'].search([('name', '=', source)])
                stage_id = self.env['crm.stage'].search([('name', '=', stage)])

                crm_val = {
                    'name': opportunity,
                    'expected_revenue': expected_revenue,
                    'probability': probability,
                    'partner_id': partner_id.id,
                    'email_from': email,
                    'phone': phone,
                    'date_deadline': expected_closing,
                    'user_id': user_id.id,
                    'team_id': team_id.id,
                    'as_9100_form': as_9100_from,
                    'priority': priority,
                    'tag_ids': [(6, 0, tag_ids.ids)],
                    'partner_name': customer_name,
                    'street': street,
                    'street2': street2,
                    'city': city,
                    'state_id': state_id.id,
                    'zip': zip,
                    'country_id': country_id.id,
                    'website': website,
                    'contact_name': contact_name,
                    'title': title,
                    'function': job_position,
                    'mobile': mobile,
                    'campaign_id': campaign_id.id,
                    'source_id': source_id.id,
                    'day_open': days_to_assign,
                    'day_close': days_to_close,
                    'referred': referred_by,
                    'stage_id': stage_id.id,
                }
                crm_id = self.env['crm.lead'].sudo().create(crm_val)
                print("crm_val", crm_id)
