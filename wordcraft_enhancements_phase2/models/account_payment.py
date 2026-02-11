from odoo import models

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_save_and_post(self):
        self.ensure_one()

        # Save happens automatically before object method
        self.action_post()

        return {'type': 'ir.actions.act_window_close'}
