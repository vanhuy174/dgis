
from odoo import api, fields, models

class User(models.Model):

    _inherit = 'res.users'
    _description = ''

    seq_number = fields.Char(string='seq id')
    name = fields.Char(string='Họ tên')
    login = fields.Char( string='Địa chỉ Email')
    phone = fields.Char( string='Số điện thoại')
    key_user = fields.Selection(
        string='Chức vụ',
        selection=[ ('admin', 'Admin'),
                    ('manage', 'Quản lý'),
                    ('nvcskh', 'Nhân viên chăm sóc khách hàng'),
                    ('nvinfolife', 'Nhân viên Infolife'),
                    ], required=False,)

class partner(models.Model):

    _inherit = 'res.partner'
    _translate = True

    key_user = fields.Selection(
        string='Chức vụ',
        selection=[('admin', 'Admin'),
                   ('manage', 'Quản lý'),
                   ('nvcskh', 'Nhân viên chăm sóc khách hàng'),
                   ('nvinfolife', 'Nhân viên Infolife'),
                   ], required=False, )