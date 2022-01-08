from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_a_customer = fields.Boolean(string="Is a Customer")
    is_a_vendor = fields.Boolean(string="Is a Vendor")
    id = fields.Integer(string="ID") # No Use
    id_custom = fields.Integer(string="ID")
    # created_by_custom = fields.Many2one(comodel_name="res.users", string="Created by")
