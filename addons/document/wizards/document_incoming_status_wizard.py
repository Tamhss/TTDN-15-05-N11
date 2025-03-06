from odoo import models, fields, api

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
        """Cập nhật trạng thái của văn bản đến"""
        self.document_id.write({'state': self.new_state})
        return {'type': 'ir.actions.act_window_close'}
