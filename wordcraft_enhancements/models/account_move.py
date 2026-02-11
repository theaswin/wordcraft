from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    def button_cancel(self):
        if not self.env.user.has_group(
            'wordcraft_enhancements.group_access_to_cancel_entries'
        ):
            raise UserError(_("You are not allowed to cancel invoices."))

        return super().button_cancel()
