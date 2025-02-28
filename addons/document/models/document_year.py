from odoo import models, fields

class DocumentYear(models.Model):
    _name = 'document_year'
    _description = 'Document Year'

    name = fields.Char(string='Năm', required=True)
    description = fields.Text(string='Mô tả')
