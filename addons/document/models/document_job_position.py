from odoo import models, fields

class JobPosition(models.Model):
    _name = 'document_job_position'
    _description = 'Job Position'

    name = fields.Char(string='Tên chức vụ', required=True)
    description = fields.Text(string='Mô tả')