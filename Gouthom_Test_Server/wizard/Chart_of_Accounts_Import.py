from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class AccountAccountWizard(models.TransientModel):
    _name = "account.account.wizard"
    _description = "Account Account Wizard"

    load_file = fields.Binary("Load File")

    def import_coa_data(self):
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
                code = value[0]
                name = value[1]
                type = value[2]
                tags = value[3]
                default_taxes = value[4]
                company = value[5]
                allow_reconciliation = value[6]

                user_type_id = self.env['account.account.type'].search([('name', '=', type)])
                company_id = self.env['res.company'].search([('name', '=', company)])
                tag_ids = self.env['account.account.tag'].search([('name', '=', tags)])
                tax_ids = self.env['account.tax'].search([('name', '=', default_taxes)])

                search_name = self.env['account.account'].search([('name', '=', name), ('code', '=', code)])

                if not search_name:
                    coa_val = {
                        'code': code,
                        'name': name,
                        'user_type_id': user_type_id.id,
                        'tag_ids': [(6, 0, tag_ids.ids)],
                        'tax_ids': [(6, 0, tax_ids.ids)],
                        'company_id': company_id.id,
                        'reconcile': True if allow_reconciliation == "True" else False,
                    }
                    coa_id = self.env['account.account'].create(coa_val)
                else:
                    search_name.write({
                        'code': code,
                        'name': name,
                        'user_type_id': user_type_id.id,
                        'tag_ids': [(6, 0, tag_ids.ids)],
                        'tax_ids': [(6, 0, tax_ids.ids)],
                        'company_id': company_id.id,
                        'reconcile': True if allow_reconciliation == "True" else False,
                    })