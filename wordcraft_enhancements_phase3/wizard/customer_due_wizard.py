from odoo import models, fields, api

class CustomerDueWizard(models.TransientModel):
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

    

    user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        related="partner_id.user_id", readonly=True 
    )

    amount_due = fields.Float(
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
    plan_id = fields.Many2one('account.analytic.plan', string="Analytic Plan")
    debit = fields.Monetary(string="Debit", readonly=True)
    credit = fields.Monetary(string="Credit",readonly=True)    
    balance = fields.Monetary(string="Balance", readonly=True)

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
                
    @api.onchange('partner_id')
    def _compute_due_amount(self):
        for rec in self:
            rec.amount_due = sum(self.env['account.move'].search(
                [('partner_id', '=', rec.id), ('payment_state', '!=', 'paid'),
                 ('state','!=','cancel'),
                ('move_type', '=', 'out_invoice')]).mapped('amount_residual'))
            rec.mobile = rec.partner_id.mobile
            rec.phone = rec.partner_id.phone
            rec.email = rec.partner_id.email

