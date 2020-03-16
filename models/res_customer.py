
from odoo import api, fields, models

class Customers(models.Model):

    _name = 'cm.customer'
    _description = ''

    Custom_ID = fields.Char(string='ID')
    image = fields.Binary('Picture', attachment=True)
    ho_ten = fields.Char(string='Họ tên')
    email = fields.Char(string='Địa chỉ Email')
    so_dien_thoai = fields.Char(string='Số điện thoại')
    gioi_tinh = fields.Selection(
        string='Giới tính',
        selection=[('nam', 'Nam'),
                   ('nu', 'Nữ'),
                   ], required=False, )
    ngay_sinh = fields.date(string='Ngày sinh')
    cmnd = fields.Char(string='Số CMND')
    diachi = fields.Char(string='Địa chỉ')
    nghe_nghiep = fields.Char(string='Nghề Nghiệp')
    tt_honnhan = fields.Char(string='Tình trạng hôn nhân')
    muc_thu_nhap = fields.Char(string='Mức thu nhập')
    so_nv = fields.Integer(string='Số nhân viên')
    ky_nang = fields.Char(string='Kỹ năng')
    trinh_do = fields.Char(string='Trình độ chuyên môn')
    so_thich = fields.Char(string='Sở thích')
    lien_he_ten = fields.Char(string='Họ tên')
    lien_sdt = fields.Char(string='Số điện thoại')
    lien_emil = fields.Char(string="Email")
    lien_dia_chi = fields.Char(string='Dịa chỉ')
