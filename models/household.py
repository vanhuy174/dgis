import base64
from odoo import tools
from odoo import models, fields, api
from odoo.modules.module import get_module_resource

class Household(models.Model):
    _name = 'cmsw.household'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _inherits = {'cmsw.address': 'address_id'}
    _rec_name = 'name'

    #household
    name = fields.Char()
    name_seq = fields.Char(string='Mã hộ gia đình', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: ('New'))

    #company
    tax_id = fields.Char(string='Mã số thuế')
    director = fields.Char(string="Giám đốc")

    is_company = fields.Boolean(string='Is a Company', default=False,
                                help="Check if the contact is a company, otherwise it is a person")
    company_type = fields.Selection(string='Company Type',
                                    selection=[('person', 'Cá nhân'), ('company', 'Tổ chức')],
                                    compute='_compute_company_type', inverse='_write_company_type')

    phone = fields.Char(string="Số điện thoại")
    email = fields.Char(string='Email')
    cmnd = fields.Char(string='Số CMND', required=False)
    date_allow = fields.Date(string='Ngày cấp', required=False)
    # address
    apart_num = fields.Char(string="Số nhà")
    street = fields.Char(string="Tổ/Xóm")
    address_id = fields.Many2one(comodel_name='cmsw.address', string='Phường/Xã',  required=True,)
    province = fields.Char(string='Tỉnh',  required=True,)
    district = fields.Char(string='Huyện',  required=True,)
    area = fields.Selection(
        string='Khu vực',
        selection=[('vip', 'Khu vực 1'),
                   ('normal', 'Khu vực 2'),
                   ('hard', 'Khu vực 3')],
        required=True, )
    pur_use = fields.Selection(
        string='Thuộc đối tượng sử dụng',
        selection=[('SH', 'Sinh hoạt các hộ dân'),
                   ('SX', 'Nước sử dụng cho sản sản xuất vật chất tại các công ty, doanh nghiệp và các đơn vị hoạt động sản xuất kinh doanh'),
                   ('HC', 'Cơ quan hành chính, sự nghiệp, công cộng'),
                   ('DV', 'Nước sử dụng cho hoạt động kinh doanh, dịch vụ')],
        required=False, )
    user_num = fields.Integer(string='Số người sử dụng', required=True)
    water_meter_number = fields.Char(string='Số công tơ', required=True)
    description = fields.Text( string="Ghi chú")
    bill_id = fields.One2many(
        comodel_name='cmsw.bill',
        inverse_name='household_id',
        string='Bill_id',
        required=False)
    amount_water_id = fields.One2many( comodel_name='cmsw.amount_of_water', inverse_name='household_id', string='Tháng sử dụng nước', required=False)
    member_of_fam = fields.One2many(
        comodel_name='cmsw.member_family',
        inverse_name='household_id',
        string='Thành viên',
        required=False)

    @api.model
    def _lang_get(self):
        return self.env['res.lang'].get_installed()

    # customer language
    lang = fields.Selection(_lang_get, string='Language',
                            help="All tanghe emails and documents sent to this contact will be translated in this language.")
    @api.onchange('address_id')
    def _onchange_address(self):
        if self.address_id.province:
            self.province = self.address_id.province
        if self.address_id.district:
            self.district = self.address_id.district
        if self.address_id.area:
            self.area = self.address_id.area

    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            if 'company_id' in vals:
                vals['name_seq'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'cmsw.household') or ('New')
            else:
                vals['name_seq'] = self.env['ir.sequence'].next_by_code('cmsw.household') or ('New')
        result = super(Household, self).create(vals)
        return result

    @api.depends('is_company')
    def _compute_company_type(self):
        for customer in self:
            customer.company_type = 'company' if customer.is_company else 'person'

    def _write_company_type(self):
        for customer in self:
            customer.is_company = customer.company_type == 'company'

    @api.onchange('company_type')
    def onchange_company_type(self):
        self.is_company = (self.company_type == 'company')

    @api.model
    def _default_image(self):
        """read image and set it by default:"""
        image_path = get_module_resource('custom_water', 'static/src/img', 'male.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))

    image = fields.Binary(
        "Avatar", default=_default_image, attachment=True,
        help="This field holds the image used as photo for the student, limited to 1024x1024px.")