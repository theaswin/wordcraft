from odoo import models, fields, api

class CustomerDueWizard(models.Model):
    _name = 'customer.due.wizard'
    _description = 'Customer Due Wizard'

    partner_id = fields.Many2one(
        'res.partner',
        string="Customer",
        required=True,
        domain="[('customer_rank', '>', 0)]"
    )

    mobile = fields.Char(string="Mobile", readonly=True)
    phone = fields.Char(string="Phone", readonly=True)
    email = fields.Char(string="Email", readonly=True)
    analytic_account_ids = fields.Many2many(
        comodel_name='account.analytic.account',
        relation='customer_due_wizard_analytic_rel',
        column1='wizard_id',
        column2='analytic_account_id',
        string='Analytic Accounts',
        readonly=True,
        help='All analytic accounts linked to this customer'
    )
    city = fields.Char(string="City")

    

    user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        related="partner_id.user_id", readonly=True 
    )

    amount_due = fields.Monetary(
        string="Amount Due",
    )

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string="Analytic Account"
    )

    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id
    )
    sale_id = fields.Many2one('sale.order', string="Sale Order")
    plan_id = fields.Many2one('account.analytic.plan', string="Analytic Plan")
    debit = fields.Monetary(string="Debit", readonly=True)
    credit = fields.Monetary(string="Credit",readonly=True)    
    balance = fields.Monetary(string="Balance", readonly=True)
    credit_tag_ids = fields.Many2many(
        comodel_name='cred.tag',
        relation='res_partner_cred_tag_rel',
        column1='partner_id',
        column2='tag_id',
        string='Credit Tags'
    )
    
    @api.onchange('credit_tag_ids')
    def _onchange_credit_tag_ids(self):
        if self.partner_id:
            self.partner_id.credit_tag_ids = [
                (6, 0, self.credit_tag_ids.ids)
            ]

    @api.onchange('analytic_account_id')
    def compute_plan(self):
        for rec in self:
            if rec.analytic_account_id:
                rec.debit = rec.analytic_account_id.debit
                rec.credit = rec.analytic_account_id.credit
                rec.balance = rec.analytic_account_id.balance
            else:
                rec.debit = 0.0
                rec.credit = 0.0
                rec.balance = 0.0
