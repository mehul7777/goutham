from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_po = fields.Char(string="Customer PO#")
    oem_code = fields.Char(string="OEM#")
    project_start_date = fields.Date(string="Project Start Date")
    project_end_date = fields.Date(string="Project end Date")
    point_contact = fields.Many2one(comodel_name="res.partner")
    project_manager = fields.Many2one(comodel_name="res.users")
    can_be_used_for_forecast = fields.Boolean(string="Can be used for Forecast")
    appear_on_pdf = fields.Boolean(string="Appear on PDF")
    point_of_contact_po = fields.Char(string="Point of Contact PO#")
    notes = fields.Text(string="Notes")
    planned_date = fields.Datetime(string="Planned Date")
    requested_date = fields.Datetime(string="Requested Date")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_oem_code = fields.Char(string="OEM#")
    warehouse_id = fields.Many2one(comodel_name="stock.warehouse")