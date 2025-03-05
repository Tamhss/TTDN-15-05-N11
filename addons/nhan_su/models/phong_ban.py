from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _order = 'ma_phong_ban'
    _rec_name = 'ten_phong_ban'
    _sql_constraints = [
        ('unique_ma_phong_ban', 'UNIQUE(ma_phong_ban)', 'Mã phòng ban phải là duy nhất!')
    ]


    ma_phong_ban = fields.Char("Mã phòng ban", required=True, index=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    chuc_vu_ids = fields.One2many('chuc_vu', 'phong_ban_id', string="Chức vụ")
    nhan_vien_ids = fields.One2many('nhan_vien', 'phong_ban_id', string="Nhân viên")
