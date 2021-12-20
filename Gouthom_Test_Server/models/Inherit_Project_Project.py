from odoo import api, fields, models


class ProProject(models.Model):
    _inherit = "project.project"

    allow_timesheets = fields.Boolean(string="Allow timesheets")
    allow_forecast = fields.Boolean(string="Allow forecast")