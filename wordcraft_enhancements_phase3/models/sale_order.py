import io
import json
import xlsxwriter
from odoo import models, fields, api
from odoo.tools import json_default
from datetime import timedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_tag_ids = fields.Many2many(
        'res.partner.category',
        'project_partner_category_rel',
        'project_id',
        'category_id',
        string="Customer Tags")

    def sale_report_excel(self):
        report_name = 'Sales Order Report'
        if len(self) > 1:
            report_name = f'Sales Order Report ({len(self)} orders)'
        elif len(self) == 1:
            report_name = f'Sales Order Report - {self.name}'

        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'sale.order',
                'options': json.dumps({'ids': self.ids}, default=json_default),
                'output_format': 'xlsx',
                'report_name': report_name,
            },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, options):
        # The controller passes options which contains the IDs
        ids = options.get('ids', [])
        records = self.browse(ids).sorted('name')
        
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Sales Orders')
        
        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D3D3D3',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        cell_format = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter'
        })
        amount_format = workbook.add_format({
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#,##0.00'
        })

        # Headers based on screenshot
        headers = [
            'Number', 'Order Date', 'Delivery Date', 'Expected Date', 'Customer',
            'Salesperson', 'Activities', 'Sales Team', 'Untaxed Amount', 'Taxes',
            'Total', 'Delivery Status', 'Invoice Status', 'Tags'
        ]
        
        # Set column widths
        col_widths = [20, 20, 20, 20, 30, 20, 15, 15, 15, 10, 10, 15, 15, 20]
        for i, width in enumerate(col_widths):
            sheet.set_column(i, i, width)

        # Write header
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, header_format)

        # Write data
        row_num = 1
        for order in records:
            sheet.write(row_num, 0, order.name or '', cell_format)
            sheet.write(row_num, 1, order.date_order.strftime('%Y-%m-%d %H:%M:%S') if order.date_order else '', cell_format)
            sheet.write(row_num, 2, order.commitment_date.strftime('%Y-%m-%d %H:%M:%S') if order.commitment_date else '', cell_format)
            sheet.write(row_num, 3, order.expected_date.strftime('%Y-%m-%d %H:%M:%S') if order.expected_date else '', cell_format)
            sheet.write(row_num, 4, order.partner_id.name or '', cell_format)
            sheet.write(row_num, 5, order.user_id.name or '', cell_format)
            sheet.write(row_num, 6, '', cell_format) # Activities
            sheet.write(row_num, 7, order.team_id.name or '', cell_format)
            sheet.write(row_num, 8, order.amount_untaxed, amount_format)
            sheet.write(row_num, 9, order.amount_tax, amount_format)
            sheet.write(row_num, 10, order.amount_total, amount_format)
            
            delivery_status = dict(order._fields['delivery_status'].selection).get(order.delivery_status, '') if 'delivery_status' in order._fields and order.delivery_status else ''
            invoice_status = dict(order._fields['invoice_status'].selection).get(order.invoice_status, '') if 'invoice_status' in order._fields and order.invoice_status else ''
            
            sheet.write(row_num, 11, delivery_status, cell_format)
            sheet.write(row_num, 12, invoice_status, cell_format)
            sheet.write(row_num, 13, ', '.join(order.tag_ids.mapped('name')), cell_format)
            row_num += 1

        workbook.close()
        output.seek(0)
        xlsx_data = output.read()
        output.close()
        return xlsx_data
