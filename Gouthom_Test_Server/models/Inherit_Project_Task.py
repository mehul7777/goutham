from odoo import api, fields, models


class ProTask(models.Model):
    _inherit = "project.task"

    starting_date = fields.Datetime(string="Starting Date")
    custom_create_date = fields.Datetime(string="Created On")
    custom_task_id = fields.Integer(string="Custom Task ID")