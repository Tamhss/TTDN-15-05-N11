from odoo import models, fields

class DocumentCategory(models.Model):
    _name = 'document_category'
    _description = 'Danh mục tài liệu'

    name = fields.Char(string="Tên danh mục", required=True)
    description = fields.Text(string="Mô tả")
