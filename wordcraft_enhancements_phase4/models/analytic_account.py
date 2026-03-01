from odoo import models, fields, api, _
from collections import defaultdict


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        help='The user responsible for this analytic account.'
    )
    credit_store = fields.Float(string='Credit(Sortable)',store=True,compute='_compute_debit_credit_balance')
    debit_store = fields.Float(string='Debit(Sortable)',store=True,compute='_compute_debit_credit_balance')
    balance_store = fields.Float(string='Balance(Sortable)',store=True,compute='_compute_debit_credit_balance')




    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Set user_id from partner if not explicitly provided
            if not vals.get('user_id') and vals.get('partner_id'):
                partner = self.env['res.partner'].browse(vals['partner_id'])
                vals['user_id'] = partner.user_id.id or False

        return super().create(vals_list)
    



    @api.depends('line_ids.amount')
    def _compute_debit_credit_balance(self):
        def convert(amount, from_currency):
            return from_currency._convert(
                from_amount=amount,
                to_currency=self.env.company.currency_id,
                company=self.env.company,
                date=fields.Date.today(),
            )

        domain = [('company_id', 'in', [False] + self.env.companies.ids)]
        if self.env.context.get('from_date', False):
            domain.append(('date', '>=', self.env.context['from_date']))
        if self.env.context.get('to_date', False):
            domain.append(('date', '<=', self.env.context['to_date']))

        for plan, accounts in self.grouped('plan_id').items():
            if not plan:
                accounts.debit = accounts.credit = accounts.balance = 0
                accounts.debit_store = accounts.credit_store = accounts.balance_store = 0
                continue
            credit_groups = self.env['account.analytic.line']._read_group(
                domain=domain + [(plan._column_name(), 'in', self.ids), ('amount', '>=', 0.0)],
                groupby=[plan._column_name(), 'currency_id'],
                aggregates=['amount:sum'],
            )
            data_credit = defaultdict(float)
            for account, currency, amount_sum in credit_groups:
                data_credit[account.id] += convert(amount_sum, currency)

            debit_groups = self.env['account.analytic.line']._read_group(
                domain=domain + [(plan._column_name(), 'in', self.ids), ('amount', '<', 0.0)],
                groupby=[plan._column_name(), 'currency_id'],
                aggregates=['amount:sum'],
            )
            data_debit = defaultdict(float)
            for account, currency, amount_sum in debit_groups:
                data_debit[account.id] += convert(amount_sum, currency)

            for account in accounts:
                account.debit = -data_debit.get(account.id, 0.0)
                account.debit_store = data_debit.get(account.id, 0.0)
                account.credit = data_credit.get(account.id, 0.0)
                account.credit_store = data_credit.get(account.id, 0.0)
                account.balance = account.credit - account.debit
                account.balance_store = account.credit - account.debit
