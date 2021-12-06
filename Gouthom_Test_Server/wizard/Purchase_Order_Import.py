from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class PO1Wizard(models.TransientModel):
    _name = "po1.wizard"
    _description = "PO1 Wizard"

    load_file = fields.Binary("Load File")

    def import_po1_data(self):
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
                order_reference = value[0]
                vendor = value[1]
                vendor_reference = value[2]
                currency = value[3]
                order_date = value[4]
                scheduled_date = value[5]
                purchase_representative = value[6]
                billing_status = value[7]
                company = value[8]
                order_lines_product = value[9]
                order_lines_description = value[10]
                order_lines_scheduled_date = value[11]
                order_lines_company = value[12]
                order_lines_quantity = value[13]
                order_lines_unit_of_measure = value[14]
                order_lines_price_unit = value[15]
                order_lines_taxes = value[16]
                deliver_to = value[17]
                fiscal_position = value[18]

                c_id = self.env['res.currency'].search([('name', '=', currency)])
                part_id = self.env['res.partner'].search([('name', '=', vendor)])
                use_id = self.env['res.users'].search([('name', '=', purchase_representative)])
                com_id = self.env['res.company'].search([('name', '=', company)])
                pro_id = self.env['product.product'].search([('name', '=', order_lines_product)])
                pick_type_id = self.env['stock.picking.type'].search([('name', '=', deliver_to)])
                fis_pos_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position)])
                tax_id = self.env['account.tax'].search([('name', '=', order_lines_taxes)])
                if not part_id:
                    vendors_val = {
                        'name': vendor
                    }
                    part_id = self.env['res.partner'].create(vendors_val)

                if order_reference:
                    po_order_val = {
                        'name': order_reference,
                        'partner_id': part_id.id,
                        'partner_ref': vendor_reference,
                        'currency_id': c_id.id,
                        'order_date': order_date,
                        'schedule_date': scheduled_date,
                        'user_id': use_id.id,
                        'invoice_status': billing_status,
                        'company_id': com_id.id,
                        'picking_type_id': pick_type_id.id,
                        'fiscal_position_id': fis_pos_id.id,
                    }
                    po_id = self.env['purchase.order'].create(po_order_val)

                if not pro_id:
                    products_val = {
                        'name': order_lines_product
                    }
                    pro_id = self.env['product.product'].create(products_val)

                po_line_vals = {
                    'product_id': pro_id[0].id,
                    'name': order_lines_description,
                    'product_qty': order_lines_quantity,
                    # 'product_uom': order_lines_unit_of_measure,
                    'price_unit': order_lines_price_unit,
                    'taxes_id': tax_id.id,
                    'order_id': po_id.id
                }
                pol_id = self.env['purchase.order.line'].create(po_line_vals)
        return True

