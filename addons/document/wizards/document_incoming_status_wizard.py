from odoo import models, fields, api
from datetime import datetime

class DocumentIncomingStatusWizard(models.TransientModel):
    _name = 'document_incoming_status_wizard'
    _description = 'Cập nhật trạng thái văn bản đến'

    document_id = fields.Many2one('document_incoming', string="Văn bản đến", required=True)
    new_state = fields.Selection([
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('processed', 'Đã xử lý'),
        ('rejected', 'Từ chối'),
    ], string='Trạng thái mới', required=True)

    def action_update_status(self):
        """Cập nhật trạng thái của văn bản đến và lưu thời gian nếu đã xử lý"""
        if self.document_id:
            updates = {'state': self.new_state}

            # Nếu chọn trạng thái "Đã xử lý" và chưa có thời gian xử lý, thì lưu lại thời gian hiện tại
            if self.new_state == 'processed' and not self.document_id.processed_datetime:
                updates['processed_datetime'] = datetime.now()

            self.document_id.write(updates)

        return {'type': 'ir.actions.act_window_close'}
