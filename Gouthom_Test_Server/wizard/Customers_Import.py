from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class CustomerWizard(models.TransientModel):
    _name = "customer.wizard"
    _description = "Customer Wizard"

    load_file = fields.Binary("Load File")

    def import_customer_data(self):
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
                company_type = value[0]
                name = value[1]
                id = value[2]
                internal_reference = value[3]
                street = value[4]
                street2 = value[5]
                city = value[6]
                state = value[7]
                zip = value[8]
                country = value[9]
                tax_id = value[10]
                phone = value[11]
                mobile = value[12]
                email = value[13]
                website = value[14]
                language = value[15]
                tags = value[16]
                created_by = value[17]
                is_a_customer = value[18]
                sales_person = value[19]
                delivery_method = value[20]
                bounce = value[21]
                price_list = value[22]
                is_a_vendor = value[23]
                supplier_currency = value[24]
                barcode = value[25] or False
                company = value[26]
                fiscal_position = value[27]
                customer_location = value[28]
                vendor_location = value[29]
                account_receivable = value[30]
                account_payable = value[31]
                credit_limit = value[32]
                related_company = value[33]
                customer_payment_terms = value[34]
                vendor_payment_terms = value[35]
                customer_rank = value[36]
                supplier_rank = value[37]
                active = value[38]

                state_id = self.env['res.country.state'].search([('name', '=', state)], limit=1)
                country_id = self.env['res.country'].search([('name', '=', country)], limit=1)
                category_id = self.env['res.partner.category'].search([('name', '=', tags)], limit=1)
                create_uid = self.env['res.users'].search([('name', '=', created_by), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                user_id = self.env['res.users'].search([('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                property_delivery_carrier_id = self.env['delivery.carrier'].search([('name', '=', delivery_method)], limit=1)
                property_product_pricelist_id = self.env['product.pricelist'].search([('name', '=', price_list)], limit=1)
                property_purchase_currency_id = self.env['res.currency'].search([('name', '=', supplier_currency)], limit=1)
                company_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                property_account_position_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position)], limit=1)
                property_stock_customer_id = self.env['stock.location'].search([('name', '=', customer_location)], limit=1)
                property_stock_supplier_id = self.env['stock.location'].search([('name', '=', vendor_location)], limit=1)
                property_account_receivable_id = self.env['account.account'].search([('name', '=', account_receivable)], limit=1)
                property_account_payable_id = self.env['account.account'].search([('name', '=', account_payable)], limit=1)
                parent_id = self.env['res.partner'].search([('name', '=', related_company), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                property_payment_term_id = self.env['account.payment.term'].search([('name', '=', customer_payment_terms)], limit=1)
                property_supplier_payment_term_id = self.env['account.payment.term'].search([('name', '=', vendor_payment_terms)], limit=1)

                if name:
                    customer_val = {
                        'company_type': company_type,
                        'name': name,
                        'id_custom': id,
                        'ref': internal_reference,
                        'street': street,
                        'street2': street2,
                        'city': city,
                        'state_id': state_id.id,
                        'zip': zip,
                        'country_id': country_id.id,
                        'vat': tax_id,
                        'phone': phone,
                        'mobile': mobile,
                        'email': email,
                        'website': website,
                        'lang': language,
                        'category_id': category_id.ids,
                        'create_uid': create_uid.id,
                        'created_by_custom': create_uid.id,
                        'is_a_customer': True if is_a_customer == "True" else False,
                        'user_id': user_id.id,
                        'property_delivery_carrier_id': property_delivery_carrier_id.id,  # make this field
                        'message_bounce': bounce,
                        'property_product_pricelist': property_product_pricelist_id.id,
                        'is_a_vendor': True if is_a_vendor == "True" else False,
                        'property_purchase_currency_id': property_purchase_currency_id.id,
                        'barcode': barcode,
                        'company_id': company_id.id,
                        'property_account_position_id': property_account_position_id.id,
                        'property_stock_customer': property_stock_customer_id.id,
                        'property_stock_supplier': property_stock_supplier_id.id,
                        'property_account_receivable_id': property_account_receivable_id.id,
                        'property_account_payable_id': property_account_payable_id.id,
                        'credit_limit': credit_limit,
                        'parent_id': parent_id.id,
                        'property_payment_term_id': property_payment_term_id.id,
                        'property_supplier_payment_term_id': property_supplier_payment_term_id.id,
                        'customer_rank': customer_rank,
                        'supplier_rank': supplier_rank,
                        'active': True if active == "True" else False,
                    }
                    if company_type == "company":
                        company_obj = self.env['res.partner'].search([('name', '=', name), ('company_type', '=', 'company'), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                        if not company_obj:
                            company_obj_id = self.env['res.partner'].sudo().create(customer_val)
                            print("customer_val", company_obj_id)
                        else:
                            company_obj.sudo().write(customer_val)
                    if company_type == 'person':
                        person_obj = self.env['res.partner'].search([('name', '=', name), ('company_type', '=', 'person'), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                        if not person_obj:
                            person_obj_id = self.env['res.partner'].sudo().create(customer_val)
                            print("customer_val", person_obj_id)
                        else:
                            person_obj.sudo().write(customer_val)