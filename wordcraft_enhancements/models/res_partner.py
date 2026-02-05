from odoo import models, fields, _ , api
from odoo.exceptions import UserError
import base64
from io import BytesIO
from openpyxl import load_workbook
import base64
import csv
from io import StringIO
import openpyxl
import io
class ResPartner(models.Model):
    _inherit = "res.partner"

    mobile = fields.Char(string="Mobile")
    google_map_url = fields.Char(string="Google Map")

    category_import_file = fields.Binary(
        string="Import Categories (Excel)",
        help="XLSX columns: name, mobile, category_name"
    )
    category_import_filename = fields.Char(string="Filename")
    due_invoice_count = fields.Integer(
        string="Due Invoice Count",
        compute="_compute_due_invoice_count",
        store=False
    )

    @api.depends('invoice_ids')
    def _compute_due_invoice_count(self):
        Move = self.env['account.move']
        for rec in self:
            rec.due_invoice_count = Move.search_count([
                ('partner_id', '=', rec.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('amount_residual', '>', 0),
            ])


    def action_view_due_statement(self):
        self.ensure_one()

        invoices = self.env['account.move'].sudo().search([
            ('partner_id', '=', self.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('amount_residual', '>', 0),
        ])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Due Invoices',
            'res_model': 'account.move',
            'domain': [('id', 'in', invoices.ids)],
            'view_mode': 'list,form',
            'target': 'current',
            'context': {
                'default_partner_id': self.id,
            },
        }
    



    def action_import_partner_categories(self):
        self.ensure_one()

        if not self.category_import_file:
            raise ValueError(_("Please upload an Excel file."))

        data = base64.b64decode(self.category_import_file)
        workbook = openpyxl.load_workbook(io.BytesIO(data))
        sheet = workbook.active

        updated = 0
        skipped = 0
        max_rows = 1000
        processed = 0

        Partner = self.env['res.partner']

        # Expected headers: name | mobile
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if processed >= max_rows:
                break

            processed += 1
            print("========================",row)
            name, mobile = row[0],row[1]

            if not name or not mobile:
                skipped += 1
                continue

            partner = Partner.search([('name', '=', name),('phone','=',False)])

            if partner:
                partner.phone = str(mobile)
                updated += 1
            else:
                skipped += 1

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Import Completed"),
                "message": _("Updated: %s\nSkipped: %s") % (updated, skipped),
                "type": "success",
            }
        }
