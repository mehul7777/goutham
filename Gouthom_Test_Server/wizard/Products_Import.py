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
        pro_id = ''
        for key, value in data_dict.items():
            if key == 0:
                header_list.append(value)
            else:
                # print(value)
                internal_reference = value[0]
                name = value[1]
                can_be_sold = value[2]
                can_be_purchased = value[3]
                can_be_expensed = value[4]
                product_type = value[5]
                product_category = value[6]
                oem = value[7]
                barcode = value[8] or False
                order_planner_policy = value[9]
                version = value[10]
                created_by = value[11]
                created_on = value[12] or False
                location = value[13]
                warehouse = value[14]
                sales_price = value[15]
                loaded_cost = value[16]
                sales_person_minimum_cost = value[17]
                customer_taxes = value[18]
                tax_cloud_cost = value[19]
                cost = value[20]
                company = value[21]
                unit_of_measure = value[22]
                purchase_unit_of_measure = value[23]
                invoice_policy = value[24]
                re_invoice_policy = value[25]
                # vendor_vendor = value[26]
                # vendor_vendor_product_code = value[27]
                # vendor_product_variant = value[28]
                # vendor_minimal_quantity = value[29]
                # vendor_unit_of_measure = value[30]
                # vendor_price = value[31]
                # vendor_currency = value[32]
                # vendor_start_date = value[33] or False
                # vendor_end_date = value[34] or False
                routes = value[26]
                responsible = value[27]
                production_location = value[28]
                inventory_location = value[29]
                income_account = value[30]

                categ_id = self.env['product.category'].search([('name', '=', product_category)], limit=1) #change this before commiting replace display_name to name
                # order_planner_policy = self.env['sale.order.planning.policy'].search([('name', '=', order_planner_policy)])
                # create_uid = self.env['res.users'].search([('name', '=', created_by)])
                location_id = self.env['stock.location'].search([('name', '=', location)], limit=1)
                warehouse_id = self.env['stock.warehouse'].search([('name', '=', warehouse)], limit=1)
                company_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                uom_id = self.env['uom.uom'].search([('name', '=', unit_of_measure)], limit=1)
                uom_po_id = self.env['uom.uom'].search([('name', '=', purchase_unit_of_measure)], limit=1)
                route_ids = self.env['stock.location.route'].search([('name', '=', routes)], limit=1)
                responsible_id = self.env['res.users'].search([('name', '=', responsible), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                property_stock_production = self.env['stock.location'].search([('name', '=', production_location)], limit=1)
                property_stock_inventory = self.env['stock.location'].search([('name', '=', inventory_location)], limit=1)
                property_account_income_id = self.env['account.account'].search([('name', '=', income_account)])
                taxes_id = self.env['account.tax'].search([('name', '=', customer_taxes)], limit=1)

                create_by_id = self.env['res.users'].search([('name', '=', created_by), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                # if not create_by_id:
                #     create_by_id = self.env['res.users'].search([('name', '=', create_by), ('active', '=', False)], limit=1)
                # follower_id = self.env['res.partner'].search([('name', '=', foweller_name)])
                #
                # if name:
                #     pt_id = self.env['product.template'].search(
                #         [('name', '=', name), ('default_code', '=', internal_reference)])
                #     update_new = {
                #         'oem': oem,
                #         'loaded_cost': loaded_cost,
                #         'property_account_income_id': property_account_income_id.id,
                #         'version': version,
                #         'create_date_custom':create_date,
                #         'create_uid_custom':create_by_id.id,
                #         'can_be_expensed': can_be_expensed,
                #     }
                #     print(update_new)
                #     pt_id.write(update_new)
                #     pt_id.message_subscribe([follower_id.id])
                # else:
                #     pt_id.message_subscribe([follower_id.id])

                # vendor_name = self.env['res.partner'].search([('name', '=', vendor_vendor), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                # vendor_product_id = self.env['product.product'].search([('name', '=', vendor_product_variant)], limit=1)
                # vendor_product_uom = self.env['uom.uom'].search([('name', '=', vendor_unit_of_measure)], limit=1)
                # vendor_currency_id = self.env['res.currency'].search([('name', '=', vendor_currency)], limit=1)

                search_product = self.env['product.template'].search([('name', '=', name), ('default_code', '=', internal_reference)])


                product_val = {
                    'default_code': internal_reference,
                    'name': name,
                    'sale_ok': True if can_be_sold == "True" else False,
                    'purchase_ok': True if can_be_purchased == "True" else False,
                    'can_be_expensed': True if can_be_expensed == "True" else False,
                    'type': product_type,
                    'categ_id': categ_id.id,
                    'oem': oem,
                    'barcode': barcode,
                    # 'order_planner_policy': order_planner_policy.id,
                    'version': version,
                    'create_uid_custom': create_by_id.id,
                    'create_date_custom': created_on,
                    'location_id': location_id.id,
                    'warehouse_id': warehouse_id.id,
                    'list_price': sales_price,
                    'loaded_cost': loaded_cost,
                    'sales_person_minimum_cost': sales_person_minimum_cost,
                    'taxes_id': [(6, 0, taxes_id.ids)],
                    'standard_price': cost,
                    'company_id': company_id.id,
                    # 'uom_id': uom_id.id,
                    # 'uom_po_id': uom_po_id.id,
                    'invoice_policy': invoice_policy,
                    'expense_policy': re_invoice_policy,
                    'route_ids': route_ids.ids,
                    'responsible_id': responsible_id.id,
                    'property_stock_production': property_stock_production.id,
                    'property_stock_inventory': property_stock_inventory.id,
                    'property_account_income_id': property_account_income_id.id,
                }
                if search_product:
                    search_product.sudo().write(product_val)
                else:
                    uom_val = {
                        'uom_id': uom_id.id,
                        'uom_po_id': uom_po_id.id,
                    }
                    create_product = product_val.update(uom_val)
                    product_id = self.env['product.template'].sudo().create(create_product)
                    print("product_val", product_id)
                # lst = []
                # if name:
                #     if vendor_vendor:
                #         vendors_val = (0, 0, {
                #             'name': vendor_name.id,
                #             'product_code': vendor_vendor_product_code,
                #             'product_id': vendor_product_id.id,
                #             'min_qty': vendor_minimal_quantity,
                #             'product_uom': vendor_product_uom.id,
                #             'price': vendor_price,
                #             'currency_id': vendor_currency_id.id,
                #             'date_start': vendor_start_date,
                #             'date_end': vendor_end_date,
                #         })
                #         lst.append(vendors_val)
                #
                #     product_val = {
                #         'default_code': internal_reference,
                #         'name': name,
                #         'sale_ok': True if can_be_sold == "True" else False,
                #         'purchase_ok': True if can_be_purchased == "True" else False,
                #         'can_be_expensed': True if can_be_expensed == "True" else False,
                #         'type': product_type,
                #         'categ_id': categ_id.id,
                #         'oem': oem,
                #         'barcode': barcode,
                #         # 'order_planner_policy': order_planner_policy.id,
                #         'version': version,
                #         'create_uid_custom': create_by_id.id,
                #         'create_date_custom': created_on,
                #         'location_id': location_id.id,
                #         'warehouse_id': warehouse_id.id,
                #         'list_price': sales_price,
                #         'loaded_cost': loaded_cost,
                #         'sales_person_minimum_cost': sales_person_minimum_cost,
                #         'taxes_id': [(6, 0, taxes_id.ids)],
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
                #         'seller_ids': lst
                #     }
                #     if search_product:
                #         pro_id = search_product.write(product_val)
                #     # product_id = self.env['product.template'].create(product_val)
                #     # print("product_val", product_id)
                # else:
                #     if vendor_vendor:
                #         vendors_val = (0, 0, {
                #             'name': vendor_name.id,
                #             'product_code': vendor_vendor_product_code,
                #             'product_id': vendor_product_id.id,
                #             'min_qty': vendor_minimal_quantity,
                #             'product_uom': vendor_product_uom.id,
                #             'price': vendor_price,
                #             'currency_id': vendor_currency_id.id,
                #             'date_start': vendor_start_date,
                #             'date_end': vendor_end_date,
                #         })
                #         if search_product:
                #             lst.append(vendors_val)
                #             pro_id.write({'seller_ids': lst})
