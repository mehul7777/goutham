from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class JournalAccountWizard(models.TransientModel):
    _name = "journal.account.wizard"
    _description = "Journal Account Wizard"

    load_file = fields.Binary("Load File")

    def import_account_journal_data(self):
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
                journal_name = value[0]
                type = value[1]
                company = value[2]
                short_code = value[3]
                next_number = value[4]
                entry_sequence = value[5]
                default_debit_account = value[6]
                default_credit_account = value[7]
                currency = value[8]
                active = value[9]

                company_id = self.env['res.company'].search([('name', '=', company)])
                check_sequence_id = self.env['ir.sequence'].search([('name', '=', entry_sequence)])
                payment_debit_account_id = self.env['account.account'].search([('code', '=', default_debit_account)])
                default_credit_account_id = self.env['account.account'].search([('code', '=', default_credit_account)])
                currency_id = self.env['res.currency'].search([('name', '=', currency)])

                search_journal = self.env['account.journal'].search([('name', '=', journal_name)])

                if journal_name:
                    journals_val = {
                        'name': journal_name,
                        'type': type,
                        'default_account_id': payment_debit_account_id.id,
                        'company_id': company_id.id,
                        'code': short_code,
                        'check_next_number': next_number,
                        'check_sequence_id': check_sequence_id.id,
                        'payment_debit_account_id': payment_debit_account_id.id,
                        'payment_credit_account_id': default_credit_account_id.id,
                        'currency_id': currency_id.id,
                        'active': False if active == "False" else True,
                    }
                    if not search_journal:
                        account_journal_id = self.env['account.journal'].create(journals_val)
                    else:
                        search_journal.write(journals_val)

