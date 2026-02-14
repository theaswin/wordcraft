from odoo import models, fields, _ , api
from odoo.exceptions import UserError
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirmed_time = fields.Datetime(string="Confirmed Time", copy=False)
    deadline = fields.Datetime(string="Deadline",copy=False,default=lambda self: fields.Datetime.now() + timedelta(hours=1))
    x_external_so_id = fields.Integer(
        string="External Sale Order ID",
        index=True,
        copy=False
    )

    def action_confirm(self):
        res = super().action_confirm()

        now = fields.Datetime.now()
        for order in self:
            # set only once
            if not order.confirmed_time:
                order.confirmed_time = now

        return res


    def action_cancel(self):
        for rec in self:
            if not rec.env.user.has_group(
                'wordcraft_enhancements.group_access_to_cancel_entries'
            ):
                raise UserError(_("You are not allowed to cancel Sale Orders."))

        return super().action_cancel()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    confirmed_time = fields.Datetime(string="Confirmed Time", copy=False)
    deadline = fields.Datetime(string="Deadline",copy=False)
    x_external_sol_id = fields.Integer(
        string="External Sale Order Line ID",
        index=True,
        copy=False,
        

    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.order_id.deadline:
                rec.deadline = rec.order_id.deadline