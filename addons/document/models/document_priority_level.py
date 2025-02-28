from odoo import models, fields

class DocumentPriorityLevel(models.Model):
    _name = 'document_priority_level'
    _description = 'Document Priority Level'

    name = fields.Char(string='Độ khẩn', required=True)
    description = fields.Text(string='Mô tả')