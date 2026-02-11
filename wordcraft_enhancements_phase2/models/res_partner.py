
from odoo import models, api,_
from odoo.exceptions import UserError , ValidationError
class ResPartner(models.Model):
    _inherit = 'res.partner'


    def action_collect_advance_payment(self):
        self.ensure_one()


        journal = self.env['account.journal'].search(
            [('type', 'in', ('bank', 'cash'))],
            limit=1
        )
        if not journal:
            raise UserError("Please configure a Bank or Cash journal.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Collect Advance Payment',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
                'default_partner_type': 'customer',
                'default_payment_type': 'inbound',
                'default_journal_id': journal.id,
                'hide_confirm_button': True,   # 👈 IMPORTANT
                'hide_save_and_post_button': False,  # 👈 IMPORTANT
            }
        }
