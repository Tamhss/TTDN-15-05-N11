from odoo import models, fields

class DocumentOutgoingHistory(models.Model):
    _name = 'document_outgoing_history'
    _description = 'Lịch sử xử lý văn bản đi'
    _order = 'change_date desc'

    document_id = fields.Many2one('document_outgoing', string='Văn bản', required=True)
    state = fields.Selection([
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('processed', 'Đã xử lý'),
        ('rejected', 'Từ chối'),
    ], string='Trạng thái', required=True)
    change_date = fields.Datetime(string='Thời gian thay đổi', default=fields.Datetime.now, required=True)
    changed_by = fields.Many2one('res.users', string='Người thay đổi', default=lambda self: self.env.user, required=True)
    note = fields.Text(string='Ghi chú')

    # **Thông tin từ document_outgoing (Chỉ hiển thị, không lưu vào database)**
    document_name = fields.Char(string="Số/Ký hiệu", related="document_id.name", store=False)
    outgoing_number = fields.Char(string="Số văn bản đi", related="document_id.out_number", store=False)
    document_number = fields.Char(string="Số văn bản", related="document_id.document_number", store=False)
    document_notation = fields.Char(string="Ký hiệu", related="document_id.document_notation", store=False)
    document_type_id = fields.Many2one('document_type', string="Loại văn bản", related="document_id.document_type_id", store=False)
    document_field_id = fields.Many2one('document_field', string="Lĩnh vực", related="document_id.document_field_id", store=False)
    issuing_agency_id = fields.Many2one('document_external_agency', string="Cơ quan ban hành", related="document_id.issuing_agency_id", store=False)
    signer_id = fields.Many2one('nhan_vien', string="Người ký", related="document_id.signer_id", store=False)
    signer_position = fields.Many2one('chuc_vu', string="Chức vụ người ký", related="document_id.signer_position", store=False)
    issue_date = fields.Date(string="Ngày ban hành", related="document_id.issue_date", store=False)
    signing_date = fields.Date(string="Ngày ký", related="document_id.signing_date", store=False)
    document_year_id = fields.Many2one('document_year', string="Năm văn bản đi", related="document_id.document_year_id", store=False)
    summary = fields.Text(string="Trích yếu", related="document_id.summary", store=False)
    
    drafting_unit_id = fields.Many2one('document_internal_department', string="Đơn vị thảo", related="document_id.drafting_unit_id", store=False)
    drafter_id = fields.Many2one('nhan_vien', string="Người soạn thảo", related="document_id.drafter_id", store=False)

    copy_number = fields.Integer(string="Số bản", related="document_id.copy_number", store=False)
    page_number = fields.Integer(string="Số trang", related="document_id.page_number", store=False)
    archive_number = fields.Integer(string="Số bản lưu", related="document_id.archive_number", store=False)

    priority_level = fields.Selection([
        ('normal', 'Bình thường'),
        ('urgent', 'Khẩn'),
        ('very_urgent', 'Thượng khẩn'),
        ('express', 'Hỏa tốc'),
    ], string='Độ khẩn', related="document_id.priority_level", store=False)

    security_level = fields.Selection([
        ('public', 'Công khai'),
        ('internal', 'Nội bộ'),
        ('confidential', 'Mật'),
        ('ultra_classified', 'Tuyệt mật'),
        ('top_secret', 'Tối mật'),
    ], string='Độ mật', related="document_id.security_level", store=False)

    sending_method = fields.Selection([
        ('email', 'Email'),
        ('post', 'Bưu điện'),
        ('direct', 'Gửi trực tiếp'),
    ], string='Phương thức gửi', related="document_id.sending_method", store=False)

    creator_id = fields.Many2one('nhan_vien', string="Người nhập", related="document_id.creator_id", store=False)
    is_reply_required = fields.Boolean(string="Cần trả lời", related="document_id.is_reply_required", store=False)
    is_qppl = fields.Boolean(string="Là văn bản QPPL", related="document_id.is_qppl", store=False)

    processed_datetime = fields.Datetime(string="Ngày đã xử lý", related="document_id.processed_datetime", store=False)
