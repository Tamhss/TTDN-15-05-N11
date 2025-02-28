from odoo import models, fields

class DocumentAgencyLevel(models.Model):
    _name = 'document_agency_level'
    _description = 'Agency Level'

    name = fields.Char(string='Tên cấp cơ quan', required=True)
    description = fields.Text(string='Mô tả')