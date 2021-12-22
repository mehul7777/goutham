from odoo import api, fields, models


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    custom_id = fields.Integer(string="Employee ID")
    is_a_manager = fields.Boolean(string="Is a Manager")
    timesheet_validation_date = fields.Date(string="Timesheets Validation Date")
    timesheet_responsible_id = fields.Many2one(comodel_name="res.users", string="Timesheet Responsible")
    expense_responsible_id = fields.Many2one(comodel_name="res.users", string="Expense Responsible")
    remaining_legal_leaves = fields.Float(string="Remaining Legal Leaves")
    medical_examination_date = fields.Date(string="Medical Exam")
    manual_attendance = fields.Boolean(string="Manual Attendance")
    job_description = fields.Text(string="Job Description(F-720-003)")