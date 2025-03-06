from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DocumentOutgoing(models.Model):
    _name = 'document_outgoing'
    _description = 'Văn bản đi'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Số, ký hiệu', required=True, tracking=True)
    outgoing_number = fields.Integer(string='Số văn bản đi', tracking=True)
    document_number = fields.Char(string='Số văn bản', required=True, tracking=True)
    document_notation = fields.Char(string='Ký hiệu', required=True, tracking=True)
    register_id = fields.Many2one('document_register', string='Sổ văn bản đi', required=True)
    document_type_id = fields.Many2one('document_type', string='Loại văn bản', required=True)
    signing_date = fields.Date(string='Ngày ký', required=True)
    issue_date = fields.Date(string='Ngày ban hành', required=True)
    document_field_id = fields.Many2one('document_field', string='Lĩnh vực')
    summary = fields.Text(string='Trích yếu', required=True)
    document_year_id = fields.Many2one('document_year', string='Năm văn bản đi')
    
    signer_id = fields.Many2one('nhan_vien', string='Người ký', required=True)
    signer_position = fields.Many2one('chuc_vu', string='Chức vụ người ký', compute='_compute_signer_position', store=True)
    issuing_agency_id = fields.Many2one('document_external_agency', string='Cơ quan ban hành văn bản', required=True)

    drafting_unit_id = fields.Many2one('document_internal_department', string='Đơn vị thảo')
    drafter_id = fields.Many2one('nhan_vien', string='Người soạn thảo')
    
    copy_number = fields.Integer(string='Số bản')
    page_number = fields.Integer(string='Số trang')
    archive_number = fields.Integer(string='Số bản lưu')

    priority_level = fields.Selection([
        ('normal', 'Bình thường'),
        ('urgent', 'Khẩn'),
        ('very_urgent', 'Thượng khẩn'),
        ('express', 'Hỏa tốc'),
    ], string='Độ khẩn', default='normal')

    security_level = fields.Selection([
        ('public', 'Công khai'),
        ('internal', 'Nội bộ'),
        ('confidential', 'Mật'),
        ('ultra_classified', 'Tuyệt mật'),
        ('top_secret', 'Tối mật'),
    ], string='Độ mật', default='public')

    sending_method = fields.Selection([
        ('email', 'Email'),
        ('post', 'Bưu điện'),
        ('direct', 'Gửi trực tiếp'),
    ], string='Phương thức gửi')

    creator_id = fields.Many2one('nhan_vien', string='Người nhập')

    is_reply_required = fields.Boolean(string='Là văn bản cần trả lời')
    is_qppl = fields.Boolean(string='Là văn bản QPPL')

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Tệp đính kèm',
        help="Chọn nhiều tệp văn bản"
    )

    state = fields.Selection([
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('processed', 'Đã xử lý'),
        ('rejected', 'Từ chối'),
    ], string='Status', default='pending', tracking=True)

    processed_datetime = fields.Datetime(string='Ngày đã xử lý')

    @api.depends('signer_id')
    def _compute_signer_position(self):
        for record in self:
            record.signer_position = record.signer_id.chuc_vu_id if record.signer_id else False

    def _get_next_outgoing_number(self):
        last_record = self.search([], order="id desc", limit=1)
        next_number = (int(last_record.outgoing_number) + 1) if last_record and last_record.outgoing_number.isdigit() else 1
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

    @api.onchange('signing_date')
    def _onchange_received_date(self):
        if self.signing_date:
            year = str(self.signing_date.year)  # Lấy năm từ signing_date
            document_year = self.env['document_year'].search([('name', '=', year)], limit=1)
            if document_year:
                self.document_year_id = document_year.id
            else:
                self.document_year_id = False
                raise ValidationError(f"Năm {year} chưa tồn tại trong hệ thống. Vui lòng thêm năm trước khi tiếp tục.")
            
    @api.constrains('signing_date')
    def _check_document_year(self):
        for record in self:
            if record.signing_date:
                year = str(record.signing_date.year)
                document_year = self.env['document_year'].search([('name', '=', year)], limit=1)
                if not document_year:
                    raise ValidationError(f"Năm {year} chưa tồn tại trong hệ thống. Vui lòng thêm năm trước khi tiếp tục.")
                else:
                    record.document_year_id = document_year.id

    def action_open_status_wizard(self):
        """Mở popup cập nhật trạng thái"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cập nhật trạng thái',
            'res_model': 'document_outgoing_status_wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('document.view_document_outgoing_status_wizard_form').id,
            'target': 'new',
            'context': {'default_document_id': self.id},
        }
    
    @api.constrains('state', 'processed_datetime')
    def _check_processed_date(self):
        for record in self:
            if record.state == 'processed' and not record.processed_datetime:
                raise ValidationError("Bạn phải nhập ngày đã xử lý khi trạng thái là 'Đã xử lý'.")
