from odoo import models, fields, _
from odoo.exceptions import UserError
import base64
from io import BytesIO
from openpyxl import load_workbook


class ResPartner(models.Model):
    _inherit = 'res.partner'

    category_import_file = fields.Binary(string="Import Categories (Excel)")
    category_import_filename = fields.Char()

    def action_import_partner_categories(self):
        if not self.category_import_file:
            raise UserError(_("Please upload an Excel file."))

        wb = load_workbook(
            filename=BytesIO(base64.b64decode(self.category_import_file))
        )
        sheet = wb.active

        Partner = self.env['res.partner']
        Category = self.env['res.partner.category']

        updated = 0
        skipped = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            name, mobile, phone, category_name = row

            if not name or not category_name:
                skipped += 1
                continue

            # 🔍 Partner search
            partner = Partner.search([
                ('name', '=', name),
                ('active', '=', True)
            ], limit=1)

            if not partner:
                skipped += 1
                continue

            # 🔍 Category search
            category = Category.search([
                ('name', '=', category_name)
            ], limit=1)

            if not category:
                skipped += 1
                continue

            vals = {}

            # 📞 Copy Excel mobile → partner.phone
            if mobile:
                vals['phone'] = str(mobile)

            # 🏷 Add category safely
            vals['category_id'] = [(4, category.id)]

            partner.write(vals)
            updated += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Import Completed"),
                'message': _("Updated: %s\nSkipped: %s") % (updated, skipped),
                'type': 'success',
            }
        }
