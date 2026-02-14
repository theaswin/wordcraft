
from odoo import models, api,_ , fields
from odoo.exceptions import UserError , ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'


    related_person_id = fields.Many2one('res.users',string="Related Person")

    


