from odoo import models, fields

class ExternalAgency(models.Model):
    _name = 'document_external_agency'
    _description = 'External Agency'

    name = fields.Char(string='Tên cơ quan', required=True)
    short_name = fields.Char(string='Tên viết tắt')
    description = fields.Text(string='Mô tả')
    level_id = fields.Many2one('document_agency_level', string='Cấp cơ quan')
    address = fields.Text(string='Địa chỉ')