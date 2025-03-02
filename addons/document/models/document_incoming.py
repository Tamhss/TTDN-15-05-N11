from odoo import models, fields, api

class DocumentIncoming(models.Model):
    _name = 'document_incoming'
    _description = 'Văn bản đến'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Số / Ký hiệu', required=True, tracking=True)
    register_id = fields.Many2one('document_register', string='Sổ văn bản', required=True)
    incoming_number = fields.Integer(string='Số đến', required=True, tracking=True)
    issuing_agency_id = fields.Many2one('document_external_agency', string='Cơ quan ban hành văn bản', required=True)

    received_date = fields.Date(string='Ngày đến', required=True, tracking=True)
    issue_date = fields.Date(string='Ngày ban hành', required=True, tracking=True)
    summary = fields.Text(string='Trích yếu', required=True)

    document_type_id = fields.Many2one('document_type', string='Loại văn bản', required=True)
    document_field_id = fields.Many2one('document_field', string='Lĩnh vực')
    
    signer_id = fields.Many2one('nhan_vien', string='Người ký', required=True)
    signer_position = fields.Many2one('chuc_vu', string='Chức vụ người ký', compute='_compute_signer_position', store=True)

    nature = fields.Selection([
        ('urgent', 'Khẩn cấp'),
        ('normal', 'Bình thường'),
        ('confidential', 'Mật')
    ], string='Tính chất văn bản')

    receiving_method = fields.Selection([
        ('email', 'Email'),
        ('post', 'Bưu điện'),
        ('direct', 'Gửi trực tiếp')
    ], string='Phương thức nhận')

    creator_id = fields.Many2one('nhan_vien', string='Người nhập')

    response_document_id = fields.Many2one('document.outgoing', string='Hồi đáp của văn bản đi')

    document_file = fields.Binary(string='Tệp văn bản')
    file_name = fields.Char(string='Tên tệp')

    office_leader_id = fields.Many2one('nhan_vien', string='Lãnh đạo văn phòng')
    office_advisor_id = fields.Many2one('nhan_vien', string='Tham mưu của lãnh đạo văn phòng')

    leader_id = fields.Many2one('nhan_vien', string='Lãnh đạo')
    leader_instruction = fields.Text(string='Chỉ đạo của Lãnh đạo')

    processing_unit_id = fields.Many2one('document_internal_department', string='Đơn vị xử lý')
    processing_deadline = fields.Date(string='Hạn xử lý')
    processor_id = fields.Many2one('nhan_vien', string='Người xử lý văn bản')

    cooperating_unit_ids = fields.Many2many('document_internal_department', string='Đơn vị phối hợp xử lý')
    cooperating_user_ids = fields.Many2many(
        'nhan_vien',
        'document_incoming_cooperating_nhan_vien_rel',
        'document_incoming_id',
        'nhan_vien_id',
        string='Người phối hợp xử lý'
    )

    viewers_ids = fields.Many2many(
        'nhan_vien', 
        'document_incoming_viewers_rel',
        'document_incoming_id',
        'nhan_vien_id',
        string='Người xem để biết'
    )

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('received', 'Đã nhận'),
        ('processing', 'Đang xử lý'),
        ('completed', 'Hoàn thành')
    ], string='Trạng thái', default='draft', tracking=True)

    @api.depends('signer_id')
    def _compute_signer_position(self):
        for record in self:
            record.signer_position = record.signer_id.chuc_vu_id if record.signer_id else False

    @api.model
    def create(self, vals):
        if 'incoming_number' not in vals or not vals['incoming_number']:
            vals['incoming_number'] = self.env['ir.sequence'].next_by_code('document.incoming') or 'IN-00001'
        return super(DocumentIncoming, self).create(vals)