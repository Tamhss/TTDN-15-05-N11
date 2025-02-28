from odoo import models, fields

class PublicHoliday(models.Model):
    _name = 'document_public_holiday'
    _description = 'Public Holiday'

    name = fields.Char(string='Tên ngày lễ', required=True)
    description = fields.Text(string='Mô tả')
    date = fields.Date(string='Ngày nghỉ')