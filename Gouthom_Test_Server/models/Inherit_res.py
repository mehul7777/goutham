from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_a_customer = fields.Boolean(string="Is a Customer")
    is_a_vendor = fields.Boolean(string="Is a Vendor")
    id = fields.Integer(string="ID")