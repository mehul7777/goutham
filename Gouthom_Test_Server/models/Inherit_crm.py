from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    as_9100_form = fields.Char(string="As-9100 Form #")