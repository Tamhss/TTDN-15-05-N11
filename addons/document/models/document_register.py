from odoo import models, fields

class DocumentRegister(models.Model):
    _name = 'document_register'
    _description = 'Document Register'

    name = fields.Char(string='Tên sổ văn bản', required=True)
    description = fields.Text(string='Mô tả')

    document_incoming_ids = fields.One2many('document_incoming', 'register_id', string="Văn bản đến")
    document_outgoing_ids = fields.One2many('document_outgoing', 'register_id', string="Văn bản đi")