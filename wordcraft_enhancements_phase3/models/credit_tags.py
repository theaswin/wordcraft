from odoo import models, fields

class CreditTags(models.Model):
    _name = 'cred.tag'
    _description = 'Credit Tag'
    _order = 'name'

    name = fields.Char(
        string="Tag Name",
        required=True
    )

    color = fields.Integer(
        string="Color Index"
    )
