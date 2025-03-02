import datetime
import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'
    _order = 'ma_dinh_danh'
    _sql_constraints = [
        ('unique_ma_dinh_danh', 'UNIQUE(ma_dinh_danh)', 'Mã định danh phải là duy nhất!')
    ]

    ma_dinh_danh = fields.Char("Mã định danh", required=True, index=True)
    ho_ten = fields.Char("Họ và tên", required=True)
    ngay_sinh = fields.Date("Ngày sinh", required=True)
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email", required=True)
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", required=True)
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ", required=True)
    lich_su_cong_tac_ids = fields.One2many('lich_su_cong_tac', 'nhan_vien_id', string="Lịch sử công tác")
    chung_chi_ids = fields.One2many('chung_chi', 'nhan_vien_id', string="Chứng chỉ")

    tuoi = fields.Integer(string="Tuổi", compute='_compute_tuoi', store=True)
    thang_sinh = fields.Integer(string="Tháng sinh", compute='_compute_thang_sinh', store=True)

    
    document_signed_ids = fields.One2many(
        'document_incoming', 'signer_id',
        string="Văn bản đã ký"
    )

    document_created_ids = fields.One2many(
        'document_incoming', 'creator_id',
        string="Văn bản đã nhập"
    )

    document_processed_ids = fields.One2many(
        'document_incoming', 'processor_id',
        string="Văn bản đang xử lý"
    )

    document_lead_ids = fields.One2many(
        'document_incoming', 'leader_id',
        string="Văn bản lãnh đạo chỉ đạo"
    )

    document_cooperating_ids = fields.Many2many(
        'document_incoming', 
        'document_incoming_cooperating_nhan_vien_rel',
        'nhan_vien_id', 
        'document_incoming_id',
        string="Văn bản phối hợp xử lý"
    )

    document_viewer_ids = fields.Many2many(
        'document_incoming', 
        'document_incoming_viewers_rel',
        'nhan_vien_id', 
        'document_incoming_id',
        string="Văn bản xem để biết"
    )
    
    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        today = datetime.date.today()
        for record in self:
            if record.ngay_sinh:
                birth_date = record.ngay_sinh
                record.tuoi = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                record.tuoi = 0

    @api.depends("ngay_sinh")
    def _compute_thang_sinh(self):
        for record in self:
            record.thang_sinh = record.ngay_sinh.month if record.ngay_sinh else 0

    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Nhân viên phải từ 18 tuổi trở lên!")

    @api.constrains('email')
    def _check_email(self):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Email không hợp lệ!")

    @api.constrains('so_dien_thoai')
    def _check_so_dien_thoai(self):
        phone_regex = r'^\d{10,11}$'
        for record in self:
            if record.so_dien_thoai and not re.match(phone_regex, record.so_dien_thoai):
                raise ValidationError("Số điện thoại không hợp lệ! Phải có 10 hoặc 11 chữ số.")
            
    @api.onchange('lich_su_cong_tac_ids')
    def _onchange_lich_su_cong_tac(self):
        """ Gán tự động nhân viên vào lịch sử công tác """
        for record in self:
            for lich_su in record.lich_su_cong_tac_ids:
                if not lich_su.nhan_vien_id:
                    lich_su.nhan_vien_id = record.id

