from odoo import api, fields, models


class InheritAccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    custom_id = fields.Integer(string="ID")


class InheritAccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    custom_timesheet_id = fields.Integer(string="Custom Timesheet ID")