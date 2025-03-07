from odoo import models, fields

class DocumentIncomingHistory(models.Model):
    _name = 'document_incoming_history'
    _description = 'Lịch sử xử lý văn bản đến'
    _order = 'change_date desc'

    document_id = fields.Many2one('document_incoming', string='Văn bản đến', required=True, ondelete='cascade')
    state = fields.Selection([
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('processed', 'Đã xử lý'),
        ('rejected', 'Từ chối'),
    ], string='Trạng thái', required=True)
    changed_by = fields.Many2one('res.users', string='Người thay đổi', default=lambda self: self.env.user, readonly=True)
    change_date = fields.Datetime(string='Ngày thay đổi', default=fields.Datetime.now, readonly=True)
    note = fields.Text(string='Ghi chú')

    document_name = fields.Char(string="Số/Ký hiệu", related="document_id.name", store=False)
    incoming_number = fields.Char(string="Số đến", related="document_id.incoming_number", store=False)
    issuing_agency_id = fields.Many2one('document_external_agency', string="Cơ quan ban hành", related="document_id.issuing_agency_id", store=False)
    signer_id = fields.Many2one('nhan_vien', string="Người ký", related="document_id.signer_id", store=False)
    signer_position = fields.Many2one('chuc_vu', string="Chức vụ người ký", related="document_id.signer_position", store=False)
    received_date = fields.Date(string="Ngày đến", related="document_id.received_date", store=False)
    issue_date = fields.Date(string="Ngày ban hành", related="document_id.issue_date", store=False)
    processing_deadline = fields.Date(string="Hạn xử lý", related="document_id.processing_deadline", store=False)
    document_type_id = fields.Many2one('document_type', string="Loại văn bản", related="document_id.document_type_id", store=False)
    document_field_id = fields.Many2one('document_field', string="Lĩnh vực", related="document_id.document_field_id", store=False)
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
    receiving_method = fields.Selection([
        ('email', 'Email'),
        ('post', 'Bưu điện'),
        ('direct', 'Gửi trực tiếp')
    ], string='Phương thức nhận', related="document_id.receiving_method", store=False)
    processor_id = fields.Many2one('nhan_vien', string="Người xử lý", related="document_id.processor_id", store=False)
    processing_unit_id = fields.Many2one('document_internal_department', string="Đơn vị xử lý", related="document_id.processing_unit_id", store=False)
    cooperating_unit_ids = fields.Many2many('document_internal_department', string="Đơn vị phối hợp", related="document_id.cooperating_unit_ids", store=False)
    cooperating_user_ids = fields.Many2many('nhan_vien', string="Người phối hợp", related="document_id.cooperating_user_ids", store=False)
    viewers_ids = fields.Many2many('nhan_vien', string="Người xem", related="document_id.viewers_ids", store=False)
