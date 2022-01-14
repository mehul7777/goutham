from odoo import api, fields, models


class InheritAccountMove(models.Model):
    _inherit = "account.move"

    customer_po = fields.Char(string="Customer PO#")
    point_of_contact_id = fields.Many2one(comodel_name="res.partner", string="Point of Contact")
    point_of_contact_po = fields.Char(string="Point of Contact PO#")
    project_manager_id = fields.Many2one(comodel_name="res.users", string="Project Manager")
    account_id = fields.Many2one(comodel_name="account.account", string="Account")
    journal_entry_id = fields.Many2one(comodel_name="account.move", string="Journal Entry")
    source_document = fields.Char(string="Source Document")


class InheritAccountPayment(models.Model):
    _inherit = "account.payment"

    custom_number = fields.Char(string="Number")