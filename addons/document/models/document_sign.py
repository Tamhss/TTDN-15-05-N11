from odoo import models, fields

class DocumentSign(models.Model):
    _name = 'document_sign'
    _description = 'Chữ ký số văn bản'

    document_id = fields.Many2one('document_incoming', string="Văn bản", required=True)
    signer_id = fields.Many2one('res.users', string="Người ký", required=True)
    signed_date = fields.Datetime(string="Ngày ký", default=fields.Datetime.now)
    signature = fields.Binary(string="Chữ ký")

    def sign_document(self):
        self.signed_date = fields.Datetime.now()
