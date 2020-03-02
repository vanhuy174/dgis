
from odoo import api, fields, models

class User(models.Model):

    _inherit = 'res.users'
    _description = ''

    name = fields.Char(string='Họ tên ')
    email = fields.Char( string='Email')
    phone = fields.Char( string='Số điện thoại')
    address_id = fields.Many2many( comodel_name='cmsw.address', string='Khu vực quản lý')
    position = fields.Selection(
        string='Chức vụ',
        selection=[('nvkv', 'Nhân viên khu vực'),
                   ('nvnl', 'Nhân viên nhập liệu '), ],
        required=False, )

