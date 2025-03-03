from odoo import models, fields

class DocumentFilter(models.Model):
    _name = 'document_filter'
    _description = 'Document Filter'

    name = fields.Char(string='Tên', required=True)
    description = fields.Text(string='Mô tả')