from odoo import models, fields

class DocumentRegister(models.Model):
    _name = 'document_register'
    _description = 'Document Register'

    name = fields.Char(string='Tên sổ văn bản', required=True)
    description = fields.Text(string='Mô tả')