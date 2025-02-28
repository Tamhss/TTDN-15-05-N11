from odoo import models, fields

class DocumentIncoming(models.Model):
    _name = 'document_incoming'
    _description = 'Quản lý văn bản đến'
    _rec_name = 'name'

    name = fields.Char(string="Số hiệu văn bản", required=True)
    subject = fields.Char(string="Tiêu đề", required=True)
    date_received = fields.Date(string="Ngày nhận", required=True, default=fields.Date.today)
    sender = fields.Char(string="Người gửi", required=True)
    category_id = fields.Many2one('document_category', string="Danh mục")
    attachment_ids = fields.Many2many('ir.attachment', string="Tệp đính kèm")
    description = fields.Text(string="Nội dung")

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('in_progress', 'Đang xử lý'),
        ('approved', 'Đã duyệt'),
        ('done', 'Hoàn thành')
    ], default='draft', string="Trạng thái")

    assigned_user_id = fields.Many2one('res.users', string="Người phụ trách")
    
    def action_set_in_progress(self):
        self.state = 'in_progress'

    def action_approve(self):
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'
