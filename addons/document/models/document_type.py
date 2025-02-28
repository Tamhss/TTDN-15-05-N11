from odoo import models, fields

class DocumentType(models.Model):
    _name = 'document_type'
    _description = 'Document Type'

    name = fields.Char(string='Tên loại văn bản', required=True)
    short_name = fields.Char(string='Tên viết tắt')
    description = fields.Text(string='Mô tả')
    processing_deadline = fields.Integer(string='Hạn xử lý (ngày)')