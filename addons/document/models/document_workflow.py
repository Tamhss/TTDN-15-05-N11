from odoo import models, fields, api

class DocumentWorkflow(models.Model):
    _name = 'document_workflow'
    _description = 'Luồng xử lý văn bản'

    document_id = fields.Many2one('document_incoming', string="Văn bản", required=True)
    assigned_user_id = fields.Many2one('res.users', string="Người phụ trách", required=True)
    action = fields.Selection([
        ('review', 'Xem xét'),
        ('approve', 'Duyệt'),
        ('reject', 'Từ chối')
    ], string="Hành động", required=True)
    notes = fields.Text(string="Ghi chú")
    date_action = fields.Datetime(string="Ngày thực hiện", default=fields.Datetime.now)

    def action_approve(self):
        self.action = 'approve'

    def action_reject(self):
        self.action = 'reject'
