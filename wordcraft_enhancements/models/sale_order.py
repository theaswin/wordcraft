from odoo import models, fields, _ , api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    deadline = fields.Datetime(string="Deadline")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    deadline = fields.Datetime(string="Deadline")