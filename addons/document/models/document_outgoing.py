from odoo import models, fields

class DocumentOutgoing(models.Model):
    _name = 'document_outgoing'
    _description = 'Quản lý văn bản đi'
    _rec_name = 'name'

    name = fields.Char(string="Số hiệu văn bản", required=True)
    subject = fields.Char(string="Tiêu đề", required=True)
    date_sent = fields.Date(string="Ngày gửi", required=True, default=fields.Date.today)
    receiver = fields.Char(string="Người nhận", required=True)
    category_id = fields.Many2one('document_category', string="Danh mục")
    attachment_ids = fields.Many2many('ir.attachment', string="Tệp đính kèm")
    description = fields.Text(string="Nội dung")

    approval_state = fields.Selection([
        ('draft', 'Nháp'),
        ('waiting', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('sent', 'Đã gửi')
    ], default='draft', string="Trạng thái")

    assigned_user_id = fields.Many2one('res.users', string="Người phụ trách")

    def action_submit_for_approval(self):
        self.approval_state = 'waiting'

    def action_approve(self):
        self.approval_state = 'approved'

    def action_send(self):
        self.approval_state = 'sent'
