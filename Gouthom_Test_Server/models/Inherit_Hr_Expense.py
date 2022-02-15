from odoo import api, fields, models


class HrExpenseInherit(models.Model):
    _inherit = "hr.expense"

    custom_expense_id = fields.Integer("Custom Expense ID")
    vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor")
    sales_opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Sales Opportunity")