from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.depends('payment_type')
    def _compute_available_journal_ids(self):
        """
        Get all journals having at least one payment method for inbound/outbound depending on the payment_type.
        """
        journals = self.env['account.journal'].search([
            '|',
            ('company_id', 'parent_of', self.env.company.id),
            ('company_id', 'child_of', self.env.company.id),
            ('type', 'in', ('bank', 'cash', 'credit')),
        ])
        print("self env====",self.env.context)
        for pay in self:
            if pay.payment_type == 'inbound':
                if self.env.context.get('from_contact'):
                    allowed_ids = journals.filtered('inbound_payment_method_line_ids')
                    allowed_ids = allowed_ids - self.env.user.journal_ids
                    pay.available_journal_ids = allowed_ids
                else:
                    allowed_ids = journals.filtered('inbound_payment_method_line_ids')
                    pay.available_journal_ids = allowed_ids

            else:
                if self.env.context.get('from_contact'):
                    allowed_ids = journals.filtered('outbound_payment_method_line_ids')
                    allowed_ids = allowed_ids - self.env.user.journal_ids
                    pay.available_journal_ids = allowed_ids
                else:
                    allowed_ids = journals.filtered('outbound_payment_method_line_ids')
                    pay.available_journal_ids = allowed_ids
