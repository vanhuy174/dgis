from odoo import api, fields, models

class Address(models.Model):
    _name = 'cmsw.address'
    _description = 'Địa chỉ'
    _rec_name = 'town'

    province = fields.Char( string='Tỉnh', required=True)
    district = fields.Char(string='Quận/Huyện', required=True)
    town = fields.Char(string="Phường/Thị trấn/Xã", required=True)
    household_id = fields.One2many(comodel_name='cmsw.household', inverse_name='address_id', string='Hộ gia đình', required=False)
    area = fields.Selection(
        string='Khu vực',
        selection=[('vip', 'Khu vực 1'),
                   ('normal', 'Khu vực 2'),
                   ('hard', 'Khu vực 3')],
        required=True, )

