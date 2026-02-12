from odoo import models, fields, api ,_
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_cancel(self):
        if not self.env.user.has_group(
            'wordcraft_enhancements.group_access_to_cancel_entries'
        ):
            raise UserError(_("You are not allowed to cancel payments."))

        return super().action_cancel()
