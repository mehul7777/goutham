from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class AnalyticAccountWizard(models.TransientModel):
    _name = "analytic.account.wizard"
    _description = "Analytic Account Wizard"

    load_file = fields.Binary("Load File")

    def import_analytic_account_data(self):
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
                analytic_account = value[0]
                id = value[1]
                reference = value[2]
                customer = value[3]
                customer_id = value[4]
                group = value[5]
                company = value[6]
                currency = value[7]
                active = value[8]

                search_analytic_account = self.env['account.analytic.account'].search([('name', '=', analytic_account)])

                partner_id = self.env['res.partner'].search([('name', '=', customer), ('id_custom', '=', customer_id)])
                group_id = self.env['account.analytic.group'].search([('name', '=', group)])
                company_id = self.env['res.company'].search([('name', '=', company)])
                currency_id = self.env['res.currency'].search([('name', '=', currency)])

                analytic_account_val = {
                    'name': analytic_account,
                    'custom_id': id,
                    'code': reference,
                    'partner_id': partner_id.id,
                    'group_id': group_id.id,
                    'company_id': company_id.id,
                    'currency_id': currency_id.id,
                    'active': False if active == "False" else True
                }
                if not search_analytic_account:
                    analytic_account_id = self.env['account.analytic.account'].create(analytic_account_val)
                    print(analytic_account_id)
                else:
                    search_analytic_account.write({'active': False if active == "False" else True})
