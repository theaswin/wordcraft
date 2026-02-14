from odoo import models, fields, api
from datetime import date


class Partner(models.Model):
    _inherit = 'res.partner'
