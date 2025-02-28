from odoo import models, fields, api

class DocumentReport(models.Model):
    _name = 'document_report'
    _description = 'Báo cáo văn bản'

    name = fields.Char(string="Tên báo cáo")
    start_date = fields.Date(string="Từ ngày")
    end_date = fields.Date(string="Đến ngày")
    total_incoming = fields.Integer(string="Số văn bản đến", compute="_compute_totals")
    total_outgoing = fields.Integer(string="Số văn bản đi", compute="_compute_totals")

    @api.depends('start_date', 'end_date')
    def _compute_totals(self):
        for record in self:
            record.total_incoming = self.env['document_incoming'].search_count([
                ('date_received', '>=', record.start_date),
                ('date_received', '<=', record.end_date)
            ])
            record.total_outgoing = self.env['document_outgoing'].search_count([
                ('date_sent', '>=', record.start_date),
                ('date_sent', '<=', record.end_date)
            ])
