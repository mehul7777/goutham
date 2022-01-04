from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_po = fields.Char(string="Customer PO#")
    oem_code = fields.Char(string="OEM#")
    project_start_date = fields.Date(string="Project Start Date")
    project_end_date = fields.Date(string="Project end Date")
    point_contact = fields.Many2one(comodel_name="res.partner")
    project_manager = fields.Many2one(comodel_name="res.users")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_oem_code = fields.Char(string="OEM#")
    warehouse_id = fields.Many2one(comodel_name="stock.warehouse")