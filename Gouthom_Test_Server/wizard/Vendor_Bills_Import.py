from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class VendorBillWizard(models.TransientModel):
    _name = "vendor.bill.wizard"
    _description = "Vendor Bill Wizard"

    load_file = fields.Binary("Load File")

    def import_vendor_bill_data(self):
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
        vb_id = ''
        for key, value in data_dict.items():
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                type = value[0]
                number = value[1]
                partner = value[2]
                payment_ref = value[3]
                invoice_date = value[4]
                due_date = value[5]
                currency = value[6]
                invoice_lines_product = value[7]
                invoice_lines_description = value[8]
                invoice_lines_asset_category = value[9]
                invoice_lines_account = value[10]
                invoice_lines_analytic_account = value[11]
                invoice_lines_analytic_tags = value[12]
                invoice_lines_category = value[13]
                invoice_lines_quantity = value[14]
                invoice_lines_unit_of_measure = value[15]
                invoice_lines_unit_price = value[16]
                invoice_lines_discount = value[17]
                invoice_lines_taxes = value[18]
                journal = value[19]
                account = value[20]
                accounting_date = value[21]
                reference_or_description = value[22]
                incoterm = value[23]
                fiscal_position = value[24]
                payment_terms = value[25]
                journal_entry = value[26]
                company = value[27]
                status = value[28]

                vendor_bill_vals = {

                }