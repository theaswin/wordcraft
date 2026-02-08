from odoo import models, fields, api
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = "project.task"

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
    # Compute deadline & elapsed %
    # ------------------------------------------------------------
    @api.depends('sale_line_id.deadline', 'sale_line_id.order_id.confirmed_time')
    def _compute_deadline(self):

        for rec in self:
            rec.deadline_hrs = 0.0
            rec.color_number = 0.0

            # Required fields
            if not rec.sale_line_id or not rec.sale_line_id.deadline or not rec.sale_line_id.order_id.confirmed_time:
                continue

            # Convert to datetime
            end_utc = fields.Datetime.to_datetime(rec.sale_line_id.deadline)
            start_utc = fields.Datetime.to_datetime(rec.sale_line_id.order_id.confirmed_time)
            now_utc = fields.Datetime.now()

            # Convert to user timezone
            start_dt = fields.Datetime.context_timestamp(rec, start_utc)
            end_dt = fields.Datetime.context_timestamp(rec, end_utc)
            now_dt = fields.Datetime.context_timestamp(rec, now_utc)

            # Remaining time
            rec.deadline_hrs = rec.remaining_hours_dt(
                start_dt, end_dt, now_dt
            )

            # Elapsed percentage
            rec.color_number = rec.elapsed_percentage_dt(
                start_dt, end_dt, now_dt
            )
