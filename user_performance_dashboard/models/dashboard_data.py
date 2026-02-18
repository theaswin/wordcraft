from odoo import models, api

class DashboardData(models.AbstractModel):
    _name = 'user.performance.dashboard'
    _description = 'User Performance Dashboard Data'

    @api.model
    def get_dashboard_data(self, start_date=None, end_date=None, target_user_id=None):
        user = self.env['res.users'].browse(target_user_id) if target_user_id else self.env.user
        uid = user.id
        
        # Domain for metrics (based on dates and user)
        # Assuming customers are linked via user_id
        # Assuming incentives are payments linked via user_id on partner
        
        customer_count = self.env['res.partner'].search_count([('user_id', '=', uid)])
        
        # Incentives (Payments) logic
        payment_domain = [('state', '=', 'posted'), ('partner_id.user_id', '=', uid)]
        if start_date:
            payment_domain.append(('date', '>=', start_date))
        if end_date:
            payment_domain.append(('date', '<=', end_date))
            
        payments = self.env['account.payment'].search(payment_domain)
        payment_amount = sum(payments.mapped('amount'))
        
        # Build user list for filter (e.g., all internal users)
        all_users = self.env['res.users'].search_read([('share', '=', False)], ['id', 'name'])

        return {
            'name': user.name,
            'job_title': user.partner_id.function or 'No Job Title',
            'image_url': f'/web/image?model=res.users&id={user.id}&field=avatar_128', # Smaller for sidebar
            'customer_count': customer_count,
            'payment_amount': f"SAR {payment_amount:,.2f}",
            'all_users': all_users,
            'current_user_id': user.id,
        }
