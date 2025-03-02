from odoo import models, fields, api


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin chức vụ'
    _order = 'ma_chuc_vu'
    _sql_constraints = [
        ('unique_ma_chuc_vu', 'UNIQUE(ma_chuc_vu)', 'Mã chức vụ phải là duy nhất!')
    ]

    ma_chuc_vu = fields.Char("Mã chức vụ", required=True, index=True)
    ten_chuc_vu = fields.Char("Tên chức vụ", required=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.ten_chuc_vu))
        return result