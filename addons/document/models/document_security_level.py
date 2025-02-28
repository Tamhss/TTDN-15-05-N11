from odoo import models, fields

class DocumentSecurityLevel(models.Model):
    _name = 'document_security_level'
    _description = 'Document Security Level'

    name = fields.Char(string='Độ mật', required=True)
    description = fields.Text(string='Mô tả')