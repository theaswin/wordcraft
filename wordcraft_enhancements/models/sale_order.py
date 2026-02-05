from odoo import models, fields, _ , api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirmed_time = fields.Datetime(string="Confirmed Time", copy=False)
    deadline = fields.Datetime(string="Deadline",copy=False)



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    confirmed_time = fields.Datetime(string="Confirmed Time", copy=False)
    deadline = fields.Datetime(string="Deadline",copy=False)
