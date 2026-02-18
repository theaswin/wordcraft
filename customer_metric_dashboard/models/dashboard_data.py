from odoo import models, api

class DashboardData(models.AbstractModel):
    _name = 'customer.metric.dashboard'
    _description = 'Customer Metric Dashboard Data'

    @api.model
    def get_dashboard_data(self):
        uid = self.env.uid
        
        # Quotations
        quotations = self.env['sale.order'].search([
            ('state', 'in', ['draft', 'sent']),
            ('partner_id.user_id', '=', uid)
        ])
        quotation_count = len(quotations)
        quotation_amount = sum(quotations.mapped('amount_total'))

        # Sale Orders
        sales = self.env['sale.order'].search([
            ('state', 'in', ['sale', 'done']),
            ('partner_id.user_id', '=', uid)
        ])
        sale_count = len(sales)
        sale_amount = sum(sales.mapped('amount_total'))

        # Invoices
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'), 
            ('state', '=', 'posted'),
            ('partner_id.user_id', '=', uid)
        ])
        
        paid_invoices = invoices.filtered(lambda i: i.payment_state == 'paid')
        unpaid_invoices = invoices.filtered(lambda i: i.payment_state != 'paid')
        
        paid_invoice_count = len(paid_invoices)
        paid_invoice_amount = sum(paid_invoices.mapped('amount_total'))
        
        unpaid_invoice_count = len(unpaid_invoices)
        unpaid_invoice_amount = sum(unpaid_invoices.mapped('amount_residual'))

        # Payments
        payments = self.env['account.payment'].search([
            ('state', '=', 'posted'),
            ('partner_id.user_id', '=', uid)
        ])
        payment_count = len(payments)
        payment_amount = sum(payments.mapped('amount'))

        # Customers
        customers = self.env['res.partner'].search([('user_id', '=', uid)])
        customer_count = len(customers)

        # User Info
        user = self.env.user
        
        def format_sar(val):
            return "SAR {:,.2f}".format(val)

        return {
            'user_name': user.name,
            'user_partner_id': user.partner_id.id,
            'user_job_title': user.partner_id.function or 'N/A',
            
            'quotation_count': quotation_count,
            'quotation_amount': format_sar(quotation_amount),
            
            'sale_count': sale_count,
            'sale_amount': format_sar(sale_amount),
            
            'paid_invoice_count': paid_invoice_count,
            'paid_invoice_amount': format_sar(paid_invoice_amount),
            
            'unpaid_invoice_count': unpaid_invoice_count,
            'unpaid_invoice_amount': format_sar(unpaid_invoice_amount),
            
            'payment_count': payment_count,
            'payment_amount': format_sar(payment_amount),
            
            'customer_count': customer_count,
        }
