from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class VPIWizard(models.TransientModel):
    _name = "vpi.wizard"
    _description = "VPI Wizard"

    load_file = fields.Binary("Load File")

    def import_vpi_data(self):
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
            # try:
            if key == 0:
                header_list.append(value)
            else:
                # print(value)
                vendor = value[0]
                vendor_product_name = value[1]
                vendor_product_code = value[2]
                delivery_lead_time = value[3]
                company = value[4]
                product_template = value[5]
                price = value[6]
                minimal_quantity = value[7]
                start_date = value[8] or None
                end_date = value[9] or None
                product_variant = value[10]
                currency = value[11]

                ven_id = self.env['res.partner'].search([('name', '=', vendor)])
                com_id = self.env['res.company'].search([('name', '=', company)])
                pro_tmp_id = self.env['product.template'].search([('name', '=', product_template)])
                product_id = self.env['product.product'].search([('name', '=', product_variant)])
                currency_id = self.env['res.currency'].search([('name', '=', currency)])

                if not ven_id:
                    vendors_val = {
                        'name': vendor
                    }
                    ven_id = self.env['res.partner'].create(vendors_val)

                if not pro_tmp_id:
                    products_val = {
                        'name': product_template
                    }
                    pro_tmp_id = self.env['product.template'].create(products_val)

                vpi_val = {
                    'name': ven_id[0].id,
                    'product_name': vendor_product_name,
                    'product_code': vendor_product_code,
                    'delay': delivery_lead_time,
                    'company_id': com_id.id,
                    'product_tmpl_id': pro_tmp_id[0].id,
                    'price': price,
                    'min_qty': minimal_quantity,
                    'date_start': start_date,
                    'date_end': end_date,
                    'product_id': product_id.id,
                    'currency_id': currency_id.id,
                }

                vpi_id = self.env['product.supplierinfo'].create(vpi_val)