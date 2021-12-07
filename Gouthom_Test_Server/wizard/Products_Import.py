from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class ProductWizard(models.TransientModel):
    _name = "product.wizard"
    _description = "Product Wizard"

    load_file = fields.Binary("Load File")

    def import_product_data(self):
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
                # internal_reference = value[0]
                # name = value[1]
                # can_be_sold = value[2]
                # can_be_purchased = value[3]
                # can_be_expensed = value[4]
                # product_type = value[5]
                # product_category = value[6]
                # oem = value[7]
                # barcode = value[8]
                # order_planner_policy = value[9]
                # version = value[10]
                # created_by = value[11]
                # created_on = value[12]
                # location = value[13]
                # warehouse = value[14]
                # sales_price = value[15]
                # loaded_cost = value[16]
                # sales_person_minimum_cost = value[17]
                # tax_cloud_cost = value[18]
                # cost = value[19]
                # company = value[20]
                # unit_of_measure = value[21]
                # purchase_unit_of_measure = value[22]
                # invoice_policy = value[23]
                # re_invoice_policy = value[24]
                # routes = value[25]
                # responsible = value[26]
                # production_location = value[27]
                # inventory_location = value[28]
                # income_account = value[29]

                internal_reference = value[0]
                name = value[1]
                income_account = value[2]
                oem = value[3]
                loaded_cost = value[4]
                create_date = value[5]
                create_by = value[6]
                foweller_name = value[7]
                can_be_expensed = value[8]
                version = 1

                if can_be_expensed != '0':
                    can_be_expensed = True
                else:
                    can_be_expensed = False
                # categ_id = self.env['product.category'].search([('name', '=', product_category)]) #change this before commiting replace display_name to name
                # # order_planner_policy = self.env['sale.order.planning.policy'].search([('name', '=', order_planner_policy)])
                # create_uid = self.env['res.users'].search([('name', '=', created_by)])
                # # location_id = self.env['stock.location'].search([('name', '=', location)], limit=1)
                # # warehouse_id = self.env['stock.warehouse'].search([('name', '=', warehouse)], limit=1)
                # company_id = self.env['res.company'].search([('name', '=', company)])
                # uom_id = self.env['uom.uom'].search([('name', '=', unit_of_measure)])
                # uom_po_id = self.env['uom.uom'].search([('name', '=', purchase_unit_of_measure)])
                # route_ids = self.env['stock.location.route'].search([('name', '=', routes)])
                # responsible_id = self.env['res.users'].search([('name', '=', responsible)])
                # property_stock_production = self.env['stock.location'].search([('name', '=', production_location)], limit=1)
                # property_stock_inventory = self.env['stock.location'].search([('name', '=', inventory_location)], limit=1)
                property_account_income_id = self.env['account.account'].search([('name', '=', income_account)])

                create_by_id = self.env['res.users'].search([('name', '=', create_by)], limit=1)
                if not create_by_id:
                    create_by_id = self.env['res.users'].search([('name', '=', create_by), ('active', '=', False)], limit=1)
                follower_id = self.env['res.partner'].search([('name', '=', foweller_name)])

                if name:
                    pt_id = self.env['product.template'].search(
                        [('name', '=', name), ('default_code', '=', internal_reference)])
                    update_new = {
                        'oem': oem,
                        'loaded_cost': loaded_cost,
                        'property_account_income_id': property_account_income_id.id,
                        'version': version,
                        'create_date_custom':create_date,
                        'create_uid_custom':create_by_id.id,
                        'can_be_expensed': can_be_expensed,
                    }
                    print(update_new)
                    pt_id.write(update_new)
                    pt_id.message_subscribe([follower_id.id])
                else:
                    pt_id.message_subscribe([follower_id.id])


                # if name:
                #     product_val = {
                #         'default_code': internal_reference,
                #         'name': name,
                #         'sale_ok': can_be_sold,
                #         'purchase_ok': can_be_purchased,
                #         'can_be_expensed': can_be_expensed,
                #         'type': product_type,
                #         'categ_id': categ_id.id,
                #         'oem': oem,
                #         'barcode': barcode,
                #         # 'order_planner_policy': order_planner_policy.id,
                #         'version': version,
                #         'create_uid': create_uid.id,
                #         'create_date': created_on,
                #         # 'location_id': location_id.id,
                #         # 'warehouse_id': warehouse_id.id,
                #         'list_price': sales_price,
                #         'loaded_cost': loaded_cost,
                #         'sales_person_minimum_cost': sales_person_minimum_cost,
                #         'standard_price': cost,
                #         'company_id': company_id.id,
                #         'uom_id': uom_id.id,
                #         'uom_po_id': uom_po_id.id,
                #         'invoice_policy': invoice_policy,
                #         'expense_policy': re_invoice_policy,
                #         'route_ids': route_ids.ids,
                #         'responsible_id': responsible_id.id,
                #         'property_stock_production': property_stock_production.id,
                #         'property_stock_inventory': property_stock_inventory.id,
                #         'property_account_income_id': property_account_income_id.id,
                #     }
                #     product_id = self.env['product.template'].create(product_val)
                #     print("product_val", product_id)