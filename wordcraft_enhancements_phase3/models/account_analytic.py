from odoo import models , fields,api

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    related_person_id = fields.Many2one('res.partner', string='Related Person')

