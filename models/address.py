from odoo import api, fields, models

class Address(models.Model):
    _name = 'cmsw.address'
    _description = 'Địa chỉ'
    _rec_name = 'town'

    province = fields.Char( string='Tỉnh', required=True, default="Thái Nguyên", readonly=True, store=True)
    # district = fields.Char(string='Quận/Huyện', required=True)
    district = fields.Selection(
        string='Huyện',
        selection=[('tn', 'Thành phố Thái Nguyên'),
                   ('sc', 'Thành phố sông công'),
                   ('py', 'Thị xã Phổ Yên'),
                   ('dt', 'Đại Từ'),
                   ('dh', 'Định Hóa'),
                   ('dhi', 'Đồng Hỉ'),
                   ('pb', 'Phú Bình'),
                   ('pl', 'Phú Lương'),
                   ('vn', 'Võ Nhai'), ],
        required=False, )

    town = fields.Char(string="Phường/Thị trấn/Xã", required=True)
    household_id = fields.One2many(comodel_name='cmsw.household', inverse_name='address_id', string='Hộ gia đình', required=False)
    user_id = fields.One2many(comodel_name='res.users', inverse_name='address_id', string='Người quản lý', required=False, readonly= True)
    area = fields.Selection(
        string='Khu vực',
        selection=[('vip', 'Khu vực 1'),
                   ('normal', 'Khu vực 2'),
                   ('hard', 'Khu vực 3')],
        required=True, )

