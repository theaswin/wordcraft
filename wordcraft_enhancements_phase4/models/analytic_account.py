from odoo import models, fields, api, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        help='The user responsible for this analytic account.'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Set user_id from partner if not explicitly provided
            if not vals.get('user_id') and vals.get('partner_id'):
                partner = self.env['res.partner'].browse(vals['partner_id'])
                vals['user_id'] = partner.user_id.id or False

        return super().create(vals_list)
    



