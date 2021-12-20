from odoo import api, fields, models


class ProProject(models.Model):
    _inherit = "project.project"

    allow_timesheets = fields.Boolean(string="Allow timesheets")
    allow_forecast = fields.Boolean(string="Allow forecast")
    custom_id = fields.Integer(string="ID")
    project_type = fields.Selection([('TIP', 'TIP'),
                                     ('CIC', 'WIC'),
                                     ('PIE', 'PIE'),
                                     ('PDI', 'PDI'),
                                     ('CAM', 'CAM'),
                                     ('Internal-Administration', 'Internal-Administration'),
                                     ('CON', 'CON'),
                                     ], string="Project Type")
    custom_created_by = fields.Many2one(comodel_name="res.users", string="Created By")