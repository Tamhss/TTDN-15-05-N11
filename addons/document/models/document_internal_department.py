from odoo import models, fields

class InternalDepartment(models.Model):
    _name = 'document_internal_department'
    _description = 'Internal Department'

    name = fields.Char(string='Tên đơn vị', required=True)
    description = fields.Text(string='Mô tả')