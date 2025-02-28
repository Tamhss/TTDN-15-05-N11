from odoo import models, fields

class DocumentField(models.Model):
    _name = 'document_field'
    _description = 'Document Field'

    name = fields.Char(string='Tên lĩnh vực', required=True)
    short_name = fields.Char(string='Tên viết tắt')
    description = fields.Text(string='Mô tả')