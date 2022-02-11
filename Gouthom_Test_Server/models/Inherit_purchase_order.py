from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    custom_po_id = fields.Integer(string="Custom PO ID")