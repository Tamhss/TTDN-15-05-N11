from odoo import models, fields, api

class DocumentYear(models.Model):
    _name = 'document_year'
    _description = 'Document Year'

    name = fields.Char(string='Năm', required=True)
    description = fields.Text(string='Mô tả')

    document_incoming_ids = fields.One2many('document_incoming', 'document_year_id', string="Văn bản đến")
    incoming_count = fields.Integer(string="Số lượng văn bản đến", compute="_compute_incoming_count")

    @api.depends('document_incoming_ids')
    def _compute_incoming_count(self):
        for record in self:
            record.incoming_count = len(record.document_incoming_ids)

    document_outgoing_ids = fields.One2many('document_outgoing', 'document_year_id', string="Văn bản đi")
    outgoing_count = fields.Integer(string="Số lượng văn bản đi", compute="_compute_outgoing_count")

    @api.depends('document_outgoing_ids')
    def _compute_outgoing_count(self):
        for record in self:
            record.outgoing_count = len(record.document_outgoing_ids)
