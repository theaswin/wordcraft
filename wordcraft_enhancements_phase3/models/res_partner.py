
from odoo import models, api,_ , fields
from odoo.exceptions import UserError , ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'


    related_person_id = fields.Many2one('res.users',string="Related Person")

    credit_tag_ids = fields.Many2many(
        comodel_name='cred.tag',
        relation='res_partners_cred_tag_rel',
        column1='partners_id',
        column2='tags_id',
        string='Credit Tags'
    )




    def action_view_due_statements(self):
        self.ensure_one()

        Wizard = self.env['customer.due.wizard'].sudo()
        company = self.env.user.company_id

        partners = self.env['res.partner'].sudo().search([
            ('unreconciled_aml_ids', '!=', False)
        ])

        for partner in partners:
            amount_due = 0.0

            for aml in partner.unreconciled_aml_ids:
                if aml.company_id == company and aml.move_id.state != 'cancel':
                    amount_due += aml.result

            # 🔍 STRICT search → one partner = one wizard
            wizard = Wizard.search([
                ('partner_id', '=', partner.id),
                ('company_id', '=', company.id),
            ], limit=1)

            values = {
                'partner_id': partner.id,
                'company_id': company.id,
                'mobile': partner.mobile,
                'phone': partner.phone,
                'email': partner.email,
                'amount_due': amount_due,
                'credit_tag_ids': [(6, 0, partner.credit_tag_ids.ids)],
            }

            if wizard:
                # 🔄 UPDATE (NO duplication)
                wizard.write(values)
            else:
                # ➕ CREATE (only if not exists)
                Wizard.create(values)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Due Statements',
            'res_model': 'customer.due.wizard',
            'view_mode': 'list',
            'context': {
                'search_default_group_salesperson': 1,
            }
        }
    
    
    @api.model
    def cron_generate_customer_due(self):
        print("Running cron to generate customer due records...")

        Wizard = self.env['customer.due.wizard'].sudo()
        company = self.env.company  # ✅ correct for cron

        partners = self.env['res.partner'].sudo().search([
            ('unreconciled_aml_ids', '!=', False)
        ])

        for partner in partners:
            amount_due = 0.0

            for aml in partner.unreconciled_aml_ids:
                if aml.company_id == company and aml.move_id.state != 'cancel':
                    amount_due += aml.result

            # 🔹 ONE record per partner (GLOBAL)
            wizard = Wizard.search([
                ('partner_id', '=', partner.id),
            ], limit=1)

            values = {
                'partner_id': partner.id,
                'mobile': partner.mobile,
                'phone': partner.phone,
                'email': partner.email,
                'amount_due': amount_due,
                'credit_tag_ids': [(6, 0, partner.credit_tag_ids.ids)],
            }

            if wizard:
                wizard.write(values)
            else:
                Wizard.create(values)

        print("Customer due cron completed successfully.")
