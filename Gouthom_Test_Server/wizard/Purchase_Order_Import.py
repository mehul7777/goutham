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
        po_id = ''
        for key, value in data_dict.items():
            if key == 0:
                header_list.append(value)
            else:
                # print(value)
                order_reference = value[0]
                vendor = value[1]
                status = value[2]
                vendor_reference = value[3]
                currency = value[4]
                order_date = value[5]
                scheduled_date = value[6]
                purchase_representative = value[7]
                billing_status = value[8]
                company = value[9]
                approval_date = value[10]
                order_lines_product = value[11]
                order_lines_description = value[12]
                order_lines_scheduled_date = value[13]
                order_lines_company = value[14]
                order_lines_analytic_account = value[15]
                order_lines_analytic_tags = value[16]
                order_lines_quantity = value[17]
                order_lines_unit_of_measure = value[18]
                order_lines_price_unit = value[19]
                order_lines_taxes = value[20]
                deliver_to = value[21]
                incoterm = value[22]
                payment_terms = value[23]
                fiscal_position = value[24]

                c_id = self.env['res.currency'].search([('name', '=', currency)])
                part_id = self.env['res.partner'].search([('name', '=', vendor)])
                use_id = self.env['res.users'].search([('name', '=', purchase_representative)])
                com_id = self.env['res.company'].search([('name', '=', company)])
                pro_id = self.env['product.product'].search([('name', '=', order_lines_product)], limit=1)
                pick_type_id = self.env['stock.warehouse'].search([('name', '=', deliver_to)]).in_type_id
                fis_pos_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position)])
                tax_id = self.env['account.tax'].search([('name', '=', order_lines_taxes)])
                incoterm_id = self.env['account.incoterms'].search([('name', '=', incoterm)])
                payment_term_id = self.env['account.payment.term'].search([('name', '=', payment_terms)])
                account_analytic_id = self.env['account.analytic.account'].search([('name', '=', order_lines_analytic_account)])
                analytic_tag_ids = self.env['account.analytic.tag'].search([('name', '=', order_lines_analytic_tags)])
                product_uom_id = self.env['uom.uom'].search([('name', '=', order_lines_unit_of_measure)])

                if not part_id:
                    vendors_val = {
                        'name': vendor
                    }
                    part_id = self.env['res.partner'].create(vendors_val)

                lst = []
                if order_reference:
                    if order_lines_product:
                        if not pro_id:
                            products_val = {
                                'name': order_lines_product
                            }
                            pro_id = self.env['product.product'].create(products_val)

                        if not account_analytic_id:
                            account_analytic_val = {
                                'name': order_lines_analytic_account
                            }
                            account_analytic_id = self.env['account.analytic.account'].create(account_analytic_val)

                        po_line_vals = (0, 0, {
                            'product_id': pro_id.id,
                            'name': order_lines_description,
                            'date_planned': order_lines_scheduled_date,
                            'account_analytic_id': account_analytic_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if len(analytic_tag_ids) else " ",
                            'product_qty': order_lines_quantity,
                            'product_uom': product_uom_id.id,
                            'price_unit': order_lines_price_unit,
                            'taxes_id': [(6, 0, tax_id.ids)],
                            # 'order_id': po_id.id
                        })
                        lst.append(po_line_vals)

                    po_order_val = {
                        'name': order_reference,
                        'partner_id': part_id.id,
                        'partner_ref': vendor_reference,
                        'currency_id': c_id.id,
                        'date_order': order_date,
                        'date_planned': scheduled_date,
                        'user_id': use_id.id,
                        'invoice_status': billing_status,
                        'company_id': com_id.id,
                        'picking_type_id': pick_type_id.id,
                        'fiscal_position_id': fis_pos_id.id,
                        'state': status,
                        'date_approve': approval_date,
                        'incoterm_id': incoterm_id.id,
                        'payment_term_id': payment_term_id.id,
                        'order_line': lst,
                    }
                    if status == "done":
                        po_id = self.env['purchase.order'].create(po_order_val)
                        print(po_id)
                else:
                    po_line_vals = (0, 0, {
                        'product_id': pro_id.id,
                        'name': order_lines_description,
                        'date_planned': order_lines_scheduled_date,
                        'account_analytic_id': account_analytic_id.id,
                        'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)],
                        'product_qty': order_lines_quantity,
                        'product_uom': product_uom_id.id,
                        'price_unit': order_lines_price_unit,
                        'taxes_id': [(6, 0, tax_id.ids)],
                        # 'order_id': po_id.id
                    })
                    if po_id:
                        lst.append(po_line_vals)
                        po_line_id = po_id.write({'order_line': lst})
                        print(po_line_id)
        return True

