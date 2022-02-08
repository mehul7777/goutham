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
                customer_id = value[4]
                email = value[5]
                phone = value[6]
                expected_closing = value[7] or False
                sales_person = value[8]
                sales_team = value[9]
                as_9100_from = value[10]
                priority = value[11]
                tags = value[12]
                customer_name = value[13]
                street = value[14]
                street2 = value[15]
                city = value[16]
                state = value[17]
                zip = value[18]
                country = value[19]
                website = value[20]
                contact_name = value[21]
                title = value[22]
                job_position = value[23]
                mobile = value[24]
                campaign = value[25]
                source = value[26]
                days_to_assign = value[27]
                days_to_close = value[28]
                referred_by = value[29]
                stage = value[30]
                type = value[31]

                partner_id = self.env['res.partner'].search([('name', '=', customer), ('id_custom', '=', customer_id), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                user_id = self.env['res.users'].search([('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                team_id = self.env['crm.team'].search([('name', '=', sales_team)], limit=1)
                tag_ids = self.env['crm.tag'].search([('name', '=', tags)])
                state_id = self.env['res.country.state'].search([('name', '=', state)], limit=1)
                country_id = self.env['res.country'].search([('name', '=', country)], limit=1)
                campaign_id = self.env['utm.campaign'].search([('name', '=', campaign)], limit=1)
                source_id = self.env['utm.source'].search([('name', '=', source)], limit=1)
                stage_id = self.env['crm.stage'].search([('name', '=', stage)])
                title_id = self.env['res.partner.title'].search([('name', '=', title)], limit=1)

                search_opportunity = self.env["crm.lead"].search([('name', '=', opportunity)])

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
                    'title': title_id.id,
                    'function': job_position,
                    'mobile': mobile,
                    'campaign_id': campaign_id.id,
                    'source_id': source_id.id,
                    # 'day_open': days_to_assign,
                    # 'day_close': days_to_close,
                    'referred': referred_by,
                    # 'stage_id': stage_id.id,
                    'type': type,
                }
                print(crm_val)
                if not search_opportunity:
                    crm_id = self.env['crm.lead'].sudo().create(crm_val)
                    days_val = {
                        'day_open': days_to_assign,
                        'day_close': days_to_close,
                    }
                    crm_id.write(days_val)
                    print("crm_val", crm_id)
