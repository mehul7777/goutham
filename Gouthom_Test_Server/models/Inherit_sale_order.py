from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_po = fields.Char(string="Customer PO#")
    oem_code = fields.Char(string="OEM#")
