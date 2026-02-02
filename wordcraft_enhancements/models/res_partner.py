from odoo import models, fields, _
from odoo.exceptions import UserError
import base64
from io import BytesIO
from openpyxl import load_workbook


class ResPartner(models.Model):
    _inherit = "res.partner"

    category_import_file = fields.Binary(
        string="Import Categories (Excel)",
        help="XLSX columns: name, mobile, category_name"
    )
    category_import_filename = fields.Char(string="Filename")

    def action_import_partner_categories(self):
        if not self.category_import_file:
            raise UserError(_("Please upload an Excel file first."))

        file_data = base64.b64decode(self.category_import_file)
        workbook = load_workbook(filename=BytesIO(file_data))
        sheet = workbook.active

        Partner = self.env["res.partner"]
        Category = self.env["res.partner.category"]

        updated = 0
        skipped = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            # ✅ SAFE column access (ignores extra columns)
            name = row[0]
            mobile = row[1]
            category_name = row[2]

            if not name or not category_name:
                skipped += 1
                continue

            partner = Partner.search([
                ("name", "=", name),
                ("active", "=", True)
            ], limit=1)

            if not partner:
                skipped += 1
                continue

            category = Category.search([
                ("name", "=", category_name)
            ], limit=1)

            if not category:
                skipped += 1
                continue

            vals = {}

            # mobile → phone
            if mobile:
                vals["phone"] = str(mobile)

            # add category (M2M safe)
            vals["category_id"] = [(4, category.id)]

            partner.write(vals)
            updated += 1

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Import Completed"),
                "message": _("Updated: %s\nSkipped: %s") % (updated, skipped),
                "type": "success",
            }
        }
