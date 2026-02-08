from odoo import models, fields, api
from datetime import timedelta


class ProjectProject(models.Model):
    _inherit = "project.project"

    # ------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------
    deadline_hrs = fields.Float(
        string="Remaining Hrs (H.MM)",
        compute="_compute_deadline",
        store=False
    )

    color_number = fields.Float(
        string="Elapsed %",
        compute="_compute_deadline",
        store=False
    )

    sale_prd_names = fields.Char(
        string="Sale Product Names",
        compute="_compute_sale_prd_names",
        store=False
    )

    # ------------------------------------------------------------
    # Remaining hours (H.MM format)
    # ------------------------------------------------------------
    def remaining_hours_dt(self, start_dt, end_dt, now_dt):
        if end_dt < start_dt:
            end_dt += timedelta(days=1)

        if now_dt < start_dt:
            now_dt += timedelta(days=1)

        total_minutes = int((end_dt - start_dt).total_seconds() // 60)
        elapsed_minutes = int((now_dt - start_dt).total_seconds() // 60)

        remaining_minutes = max(total_minutes - elapsed_minutes, 0)

        hours = remaining_minutes // 60
        minutes = remaining_minutes % 60

        return float(f"{hours}.{minutes:02d}")

    # ------------------------------------------------------------
    # Elapsed percentage
    # ------------------------------------------------------------
    def elapsed_percentage_dt(self, start_dt, end_dt, now_dt):
        if end_dt < start_dt:
            end_dt += timedelta(days=1)

        if now_dt < start_dt:
            now_dt += timedelta(days=1)

        total_seconds = (end_dt - start_dt).total_seconds()
        elapsed_seconds = (now_dt - start_dt).total_seconds()

        if total_seconds <= 0:
            return 0.0

        percent = (elapsed_seconds / total_seconds) * 100
        return max(0.0, min(percent, 100.0))

    # ------------------------------------------------------------
    # Compute deadline + percentage
    # ------------------------------------------------------------
    @api.depends('sale_order_id.confirmed_time', 'sale_order_id.deadline')
    def _compute_deadline(self):

        for rec in self:
            rec.deadline_hrs = 0.0
            rec.color_number = 0.0

            sale = rec.sale_order_id
            if not sale or not sale.confirmed_time or not sale.deadline:
                continue

            # Convert to datetime
            start_utc = fields.Datetime.to_datetime(sale.confirmed_time)
            end_utc = fields.Datetime.to_datetime(sale.deadline)
            now_utc = fields.Datetime.now()

            # Convert to user timezone
            start_dt = fields.Datetime.context_timestamp(rec, start_utc)
            end_dt = fields.Datetime.context_timestamp(rec, end_utc)
            now_dt = fields.Datetime.context_timestamp(rec, now_utc)

            # Remaining hours
            rec.deadline_hrs = rec.remaining_hours_dt(
                start_dt, end_dt, now_dt
            )

            # Elapsed percentage
            rec.color_number = rec.elapsed_percentage_dt(
                start_dt, end_dt, now_dt
            )

    # ------------------------------------------------------------
    # Sale product names
    # ------------------------------------------------------------
    @api.depends('sale_order_id.order_line')
    def _compute_sale_prd_names(self):
        for rec in self:
            if rec.sale_order_id and rec.sale_order_id.order_line:
                rec.sale_prd_names = ", ".join(
                    line.product_id.name
                    for line in rec.sale_order_id.order_line
                    if line.product_id
                )
            else:
                rec.sale_prd_names = ""
