from odoo import api, fields, models


class HrExpenseSheetInherit(models.Model):
    _inherit = "hr.expense.sheet"

    custom_expense_sheet_id = fields.Integer(string="Custom Expense Sheet ID")