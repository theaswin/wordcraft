
from odoo import models, api,_ , fields
from odoo.exceptions import UserError , ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'


    related_person_id = fields.Many2one('res.users',string="Related Person")

    


    def action_view_due_statements(self):
        self.ensure_one()

        analytic_ids = self.env['account.analytic.account'].search(
            [
                ('partner_id', '!=', False),
            ]
        )


        self.env['customer.due.wizard'].search([('create_uid','=',self.env.user.id)]).unlink()  # Clear existing wizard records

        for acc in analytic_ids:
            rec = self.env['customer.due.wizard'].create({
                'partner_id': acc.partner_id.id,
                'analytic_account_id': acc.id,
            })
            rec._compute_due_amount()  # Compute due amount for each record
            rec.compute_plan()  # Compute debit, credit, and balance for each record

        

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Due Statements',
            'res_model': 'customer.due.wizard',
            'view_mode': 'list',
            'context': {
                'search_default_group_partner': 1,
            }

        }

