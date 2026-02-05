from odoo import models, fields, _ , api
from odoo.exceptions import UserError
from datetime import datetime

class ProjectProject(models.Model):
    _inherit = "project.project"

    deadline_hrs = fields.Float(string="Deadline",compute="_compute_deadline",store=True)
    sale_prd_names = fields.Char(string="Sale Product Names", compute="_compute_sale_prd_names", 
                                 store=False)
    color_number = fields.Integer(string="Color")


    @api.depends('sale_order_id.confirmed_time', 'sale_order_id.deadline')
    def _compute_deadline(self):
        for rec in self:
            rec.color_number = 0.0

            confirmed = rec.sale_order_id.confirmed_time
            deadline = rec.sale_order_id.deadline

            if not confirmed or not deadline:
                continue

            confirmed_dt = fields.Datetime.from_string(confirmed)
            deadline_dt = fields.Datetime.from_string(deadline)
            now = fields.Datetime.now()

            total_seconds = (deadline_dt - confirmed_dt).total_seconds()

            # avoid division by zero
            if total_seconds <= 0:
                rec.color_number = 100.0
                continue

            elapsed_seconds = (now - confirmed_dt).total_seconds()

            percentage = (elapsed_seconds / total_seconds) * 100

            # allow negative and >100 values
            rec.color_number = round(percentage, 2)

        @api.depends('sale_order_id.order_line')
        def _compute_sale_prd_names(self):
            for rec in self:
                if rec.sale_order_id and rec.sale_order_id.order_line:
                    product_names = [line.product_id.name for line in rec.sale_order_id.order_line]
                    rec.sale_prd_names = ", ".join(product_names)
                else:
                    rec.sale_prd_names = ""
            
