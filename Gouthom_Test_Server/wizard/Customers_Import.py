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
                phone = value[10]
                mobile = value[11]
                email = value[12]
                website = value[13]
                language = value[14]
                tags = value[15]
                created_by = value[16]
                is_a_customer = value[17]
                sales_person = value[18]
                delivery_method = value[19]
                bounce = value[20]
                price_list = value[21]
                is_a_vendor = value[22]
                supplier_currency = value[23]
                barcode = value[24]
                company = value[25]
                fiscal_position = value[26]
                customer_location = value[27]
                vendor_location = value[28]
                account_receivable = value[29]
                account_payable = value[30]
                credit_limit = value[31]
                related_company = value[32]
                customer_payment_terms = value[33]
                vendor_payment_terms = value[34]
                customer_rank = value[35]
                supplier_rank = value[36]

                state_id = self.env['res.country.state'].search([('name', '=', state)])
                country_id = self.env['res.country'].search([('name', '=', country)])
                category_id = self.env['res.partner.category'].search([('name', '=', tags)])
                create_uid = self.env['res.users'].search([('name', '=', created_by)])
                user_id = self.env['res.users'].search([('name', '=', sales_person)])
                # property_delivery_carrier_id = self.env['delivery.carrier'].search(['name', '=', delivery_method])
                property_product_pricelist_id = self.env['product.pricelist'].search([('name', '=', price_list)])
                property_purchase_currency_id = self.env['res.currency'].search([('name', '=', supplier_currency)])
                company_id = self.env['res.company'].search([('name', '=', company)])
                property_account_position_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position)])
                property_stock_customer_id = self.env['stock.location'].search([('name', '=', customer_location)])
                property_stock_supplier_id = self.env['stock.location'].search([('name', '=', vendor_location)])
                property_account_receivable_id = self.env['account.account'].search([('name', '=', account_receivable)])
                property_account_payable_id = self.env['account.account'].search([('name', '=', account_payable)])
                parent_id = self.env['res.partner'].search([('name', '=', related_company)])
                property_payment_term_id = self.env['account.payment.term'].search([('name', '=', customer_payment_terms)])
                property_supplier_payment_term_id = self.env['account.payment.term'].search([('name', '=', vendor_payment_terms)])

                if name:
                    customer_val = {
                        'company_type': company_type,
                        'name': name,
                        'id': id,
                        'ref': internal_reference,
                        'street': street,
                        'street2': street2,
                        'city': city,
                        'state_id': state_id.id,
                        'zip': zip,
                        'country_id': country_id.id,
                        'phone': phone,
                        'mobile': mobile,
                        'email': email,
                        'website': website,
                        'lang': language,
                        'category_id': category_id.ids,
                        'create_uid': create_uid.id,
                        'is_a_customer': is_a_customer,
                        'user_id': user_id.id,
                        # 'property_delivery_carrier_id': property_delivery_carrier_id.id,  # make this field
                        'message_bounce': bounce,
                        'property_product_pricelist': property_product_pricelist_id.id,
                        'is_a_vendor': is_a_vendor,
                        'property_purchase_currency_id': property_purchase_currency_id.id,
                        # 'barcode': barcode,
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
                    }
                    if company_type == "company":
                        company_obj = self.env['res.partner'].search([('name', '=', name), ('company_type', '=', 'company')])
                        if not company_obj:
                            company_obj_id = self.env['res.partner'].sudo().create(customer_val)
                            print("customer_val", company_obj_id)
                    if company_type == 'person':
                        person_obj = self.env['res.partner'].search([('name', '=', name), ('company_type', '=', 'person')])
                        if not person_obj:
                            person_obj_id = self.env['res.partner'].sudo().create(customer_val)
                            print("customer_val", person_obj_id)