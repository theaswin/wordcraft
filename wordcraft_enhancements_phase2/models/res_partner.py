
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
        
        not_allowed_journals = self.env.user.journal_ids.ids

        print("not_allowed_journals===========",not_allowed_journals)

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
                'hide_confirm_button': True,
                'hide_save_and_post_button': False,
                'domain_journal_id': [('id', 'not in', not_allowed_journals)],
            }
        }

