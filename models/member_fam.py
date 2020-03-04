import base64

from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools

class MemberFamily(models.Model):
    _name = 'cmsw.member_family'
    _description = 'Member Family'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char( string='Họ tên', required=False)
    date_of_birth = fields.Date(string='Ngày sinh', required=False)
    gender = fields.Selection(
        string='Giới tính',
        selection=[('male', 'Nam'),
                   ('female', 'Nữ'),
                   ('other', 'Khác'), ],
        required=False, )

    # address
    apart_num = fields.Char(string="Số nhà")
    street = fields.Char(string="Tổ/Xóm")
    town = fields.Char(string="Phường/Thị trấn/Xã")
    district = fields.Char(string="Quận/Huyện")
    city = fields.Char(string="Tỉnh/Thành phố")

    job = fields.Char( string='Nghề nghiệp', required=False)
    folk = fields.Char(string='Dân tộc', required=True)
    religion = fields.Char(string='Tôn giáo', required=True)
    nation = fields.Many2one(comodel_name='res.country', string='Quốc tịch', required=True)
    cmnd = fields.Char(string='Số CMND', required=False)
    date_allow = fields.Date( string='Ngày cấp', required=False)
    household_id = fields.Many2one(
        comodel_name='cmsw.household',
        string='Thuộc hộ gia đình',
        required=True)
    relationship = fields.Char( string='Quan hệ với chủ hộ', required=False)
    description = fields.Text(
        string="Ghi chú",
        required=False)

    @api.model
    def _default_image(self):
        """read image and set it by default:"""
        image_path = get_module_resource('custom_water', 'static/src/img', 'image.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))

    image = fields.Binary(
        "Avatar", default=_default_image, attachment=True,
        help="This field holds the image used as photo for the student, limited to 1024x1024px.")

    @api.onchange('household_id')
    @api.multi
    def _onchange_address(self):
        if self.household_id.apart_num:
            self.apart_num = self.household_id.apart_num
        if self.household_id.street:
            self.street = self.household_id.street
        if self.household_id.address_id:
            self.town = self.household_id.address_id.town
        if self.household_id.district:
            self.district = self.household_id.district
        if self.household_id.province:
            self.city = self.household_id.province
