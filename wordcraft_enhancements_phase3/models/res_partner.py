
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
        partners = self.env['res.partner'].sudo().search([('unreconciled_aml_ids','!=',False)])
        Wizard = self.env['customer.due.wizard']
        Move = self.env['account.move']
        company = self.env.user.company_id
        Wizard.search([('create_uid', '=', self.env.user.id)]).unlink()
        for partner in partners:

            amount_due = 0.0
            for aml in  partner.unreconciled_aml_ids:
                if (aml.company_id == company) and (aml.move_id.state != 'cancel') :
                    amount_due += aml.result
            Wizard.create({
                'partner_id': partner.id,
                'mobile':partner.mobile,
                'phone':partner.phone,
                'email':partner.email,
                'amount_due': amount_due,
                'credit_tag_ids': [(6, 0, partner.credit_tag_ids.ids)],
            })
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
        print("Cron Job Started: Generating Customer Due Statements")
        partners = self.env['res.partner'].sudo().search([('unreconciled_aml_ids','!=',False)])
        Wizard = self.env['customer.due.wizard']
        company = self.env.user.company_id
        Wizard.search([]).unlink()
        for partner in partners:

            amount_due = 0.0
            for aml in  partner.unreconciled_aml_ids:
                if (aml.company_id == company) and (aml.move_id.state != 'cancel') :
                    amount_due += aml.result
            Wizard.create({
                'partner_id': partner.id,
                'mobile':partner.mobile,
                'phone':partner.phone,
                'email':partner.email,
                'amount_due': amount_due,
                'credit_tag_ids': [(6, 0, partner.credit_tag_ids.ids)],
            })
        