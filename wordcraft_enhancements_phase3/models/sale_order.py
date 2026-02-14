from odoo import models, fields, api
from datetime import timedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"


    customer_tag_ids = fields.Many2many(
        'res.partner.category',
        'project_partner_category_rel',
        'project_id',
        'category_id',
        string="Customer Tags")
