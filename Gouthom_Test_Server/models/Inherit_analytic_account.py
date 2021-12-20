from odoo import api, fields, models


class InheritAccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    custom_id = fields.Integer(string="ID")