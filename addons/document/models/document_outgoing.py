from odoo import models, fields, api

class DocumentOutgoing(models.Model):
    _name = 'document_outgoing'
    _description = 'Văn bản đi'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Số, ký hiệu', required=True, tracking=True)
    register_id = fields.Many2one('document_register', string='Sổ văn bản đi', required=True)
    serial_number = fields.Integer(string='Số thứ tự theo sổ', tracking=True)
    document_type_id = fields.Many2one('document_type', string='Loại văn bản', required=True)
    signing_date = fields.Date(string='Ngày ký', required=True)
    issue_date = fields.Date(string='Ngày ban hành', required=True)
    document_code = fields.Char(string='Ký hiệu văn bản')
    document_field_id = fields.Many2one('document_field', string='Lĩnh vực')
    summary = fields.Text(string='Trích yếu', required=True)
    
    signer_id = fields.Many2one('nhan_vien', string='Người ký', required=True)
    signer_position = fields.Many2one('chuc_vu', string='Chức vụ người ký', compute='_compute_signer_position', store=True)
    
    drafting_unit_id = fields.Many2one('document_internal_department', string='Đơn vị thảo')
    drafter_id = fields.Many2one('nhan_vien', string='Người soạn thảo')
    
    copy_number = fields.Integer(string='Số bản')
    page_number = fields.Integer(string='Số trang')
    archive_number = fields.Integer(string='Số bản lưu')

    priority_level_id = fields.Many2one('document_priority_level', string='Độ khẩn')
    sending_method = fields.Selection([
        ('email', 'Email'),
        ('post', 'Bưu điện'),
        ('direct', 'Gửi trực tiếp'),
    ], string='Phương thức gửi')

    security_level_id = fields.Many2one('document_security_level', string='Độ mật')

    creator_id = fields.Many2one('nhan_vien', string='Người nhập')

    is_reply_required = fields.Boolean(string='Là văn bản cần trả lời')
    is_qppl = fields.Boolean(string='Là văn bản QPPL')

    document_file = fields.Binary(string='Tệp văn bản')
    file_name = fields.Char(string='Tên tệp')

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('signed', 'Đã ký'),
        ('issued', 'Đã ban hành'),
        ('sent', 'Đã gửi'),
        ('done', 'Hoàn thành')
    ], string='Trạng thái', default='draft', tracking=True)

    @api.depends('signer_id')
    def _compute_signer_position(self):
        for record in self:
            record.signer_position = record.signer_id.chuc_vu_id if record.signer_id else False

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = self.env['ir.sequence'].next_by_code('document.outgoing') or 'OUT-00001'
        return super(DocumentOutgoing, self).create(vals)
