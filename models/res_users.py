
from odoo import api, fields, models

class User(models.Model):

    _inherit = 'res.users'
    _description = ''

    name = fields.Char(string='Họ tên ')
    login = fields.Char( string='Địa chỉ Email')
    phone = fields.Char( string='Số điện thoại')
    address_id = fields.Many2many( comodel_name='cmsw.address', string='Khu vực quản lý')
    # address_id = fields.Many2one(
    #     comodel_name='cmsw.address',
    #     string='Khu vực quản lý',
    #     required=False)
    position = fields.Selection(
        string='Chức vụ',
        selection=[ ('admin', 'Admin'),
                    ('ql', 'Quản lý'),
                    ('nvkv', 'Nhân viên khu vực'),
                    ('nvnl', 'Nhân viên nhập liệu '),
                    ], required=False )

class Parner(models.Model):

    _inherit = 'res.partner'
    _translate = True