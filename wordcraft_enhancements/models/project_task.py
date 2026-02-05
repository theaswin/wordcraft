from odoo import models, fields, _ , api
from odoo.exceptions import UserError
from datetime import datetime

class ProjectTask(models.Model):
    _inherit = "project.task"

    deadline_hrs = fields.Float(string="Deadline",compute="_compute_deadline",store=False)


    @api.depends('sale_line_id.deadline')
    def _compute_deadline(self):
        for rec in self:
            if rec.sale_line_id.deadline:
                deadline = fields.Datetime.from_string(rec.sale_line_id.deadline)
                now = fields.Datetime.now()
                diff = deadline - now

                hours = diff.total_seconds() / 3600
                rec.deadline_hrs = max(0.0, round(hours, 2))
            else:
                rec.deadline_hrs = 0.0

