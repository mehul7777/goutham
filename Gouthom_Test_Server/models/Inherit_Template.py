from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    can_be_expensed = fields.Boolean(string="Can be Expensed")
    oem = fields.Char(string="OEM#")
    order_planner_policy = fields.Many2one(comodel_name="sale.order.planning.policy", string="Order Planner Policy")
    version = fields.Integer(string="Version")
    loaded_cost = fields.Float(string="Loaded Cost")
    sales_person_minimum_cost = fields.Float(string="Sales Person Minimum Cost")
    tax_cloud_category = fields.Many2one(comodel_name="product.tic.category", string="TaxCloud Category")
    create_date_custom = fields.Datetime(string="Created On")
    create_uid_custom = fields.Many2one(comodel_name="res.users", string="Created By")
    custom_id = fields.Integer(string="Custom ID")