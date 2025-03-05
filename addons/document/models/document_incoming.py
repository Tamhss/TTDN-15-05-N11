from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DocumentIncoming(models.Model):
    _name = 'document_incoming'
    _description = 'Văn bản đến'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Số / Ký hiệu', required=True, tracking=True)
    register_id = fields.Many2one('document_register', string='Sổ văn bản', required=True)
    incoming_number = fields.Char(string='Số đến', required=True, tracking=True, default=lambda self: self._get_next_incoming_number(), readonly=1)
    document_number = fields.Char(string='Số văn bản', required=True, tracking=True)
    document_notation = fields.Char(string='Ký hiệu', required=True, tracking=True)
    issuing_agency_id = fields.Many2one('document_external_agency', string='Cơ quan ban hành văn bản', required=True)

    received_date = fields.Date(string='Ngày đến', required=True, tracking=True)
    document_year_id = fields.Many2one('document_year', string='Năm văn bản đến')
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

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Tệp đính kèm',
        help="Chọn nhiều tệp văn bản"
    )

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
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('processed', 'Đã xử lý'),
        ('rejected', 'Từ chối'),
    ], string='Status', default='pending', tracking=True)

    @api.depends('signer_id')
    def _compute_signer_position(self):
        for record in self:
            record.signer_position = record.signer_id.chuc_vu_id if record.signer_id else False

    def _get_next_incoming_number(self):
        last_record = self.search([], order="id desc", limit=1)
        next_number = (int(last_record.incoming_number) + 1) if last_record and last_record.incoming_number.isdigit() else 1
        return str(next_number)
    
    @api.onchange('document_type_id', 'issuing_agency_id')
    def _onchange_document_notation(self):
        if self.document_type_id and self.issuing_agency_id:
            # Lấy short_name của loại văn bản và lĩnh vực
            doc_type_short_name = self.document_type_id.short_name if self.document_type_id else ''
            issuing_agency_short_name = self.issuing_agency_id.short_name if self.issuing_agency_id else ''
            
            # Cập nhật giá trị cho trường 'name'
            self.document_notation = f"{doc_type_short_name}-{issuing_agency_short_name}"
        else:
            # Nếu thiếu thông tin, đặt giá trị mặc định
            self.document_notation = ''

    @api.onchange('document_number', 'document_notation')
    def _onchange_name(self):
        if self.document_number and self.document_notation:
            self.name = f"{self.document_number}/{self.document_notation}"
        else:
            # Nếu thiếu thông tin, đặt giá trị mặc định
            self.name = ''

    @api.onchange('received_date')
    def _onchange_received_date(self):
        if self.received_date:
            year = str(self.received_date.year)  # Lấy năm từ received_date
            document_year = self.env['document_year'].search([('name', '=', year)], limit=1)
            if document_year:
                self.document_year_id = document_year.id
            else:
                self.document_year_id = False
                raise ValidationError(f"Năm {year} chưa tồn tại trong hệ thống. Vui lòng thêm năm trước khi tiếp tục.")
            
    @api.constrains('received_date')
    def _check_document_year(self):
        for record in self:
            if record.received_date:
                year = str(record.received_date.year)
                document_year = self.env['document_year'].search([('name', '=', year)], limit=1)
                if not document_year:
                    raise ValidationError(f"Năm {year} chưa tồn tại trong hệ thống. Vui lòng thêm năm trước khi tiếp tục.")
                else:
                    record.document_year_id = document_year.id