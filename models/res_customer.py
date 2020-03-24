import base64
import uuid
from email.policy import default

from odoo.modules.module import get_module_resource
from odoo import tools
from odoo import api, fields, models, exceptions
from datetime import datetime, timedelta

class Customers(models.Model):

    _name = 'dgis.customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = ''
    _rec_name = 'ho_ten'

    tuoi = fields.Boolean(string='Tuổi', default=False, compute='get_tuoi')
    Custom_ID = fields.Char(string='ID', copy=False, readonly=True,
                         index=True, default='New')
    file_phan_tich = fields.Binary(
        "File sau phân tích ", attachment=True, compute='get_file_phan_tich')
    filename = fields.Char("Image Filename", compute='get_file_phan_tich')
    ho_ten = fields.Char(string='Họ tên', required=True,)
    email = fields.Char(string='Địa chỉ Email', required=True,)
    so_dien_thoai = fields.Char(string='Số điện thoại', required=True)
    gioi_tinh = fields.Selection(
        string='Giới tính',
        selection=[('nam', 'Nam'),
                   ('nu', 'Nữ'),
                   ], required=True, )
    ngay_sinh = fields.Datetime(string='Ngày sinh',select=True, default=lambda self: fields.datetime.now())
    cmnd = fields.Char(string='Số CMND')
    diachi = fields.Char(string='Địa chỉ', required=True)
    nghe_nghiep = fields.Char(string='Nghề Nghiệp')
    tt_honnhan = fields.Selection(string='Tình trạng hôn nhân',
        selection=[('dt', 'Độc thân'),
                   ('dkh', 'Đã kết hôn'),
                   ('dlh', 'Đã ly hôn'),
                   ], required=False,)
    muc_thu_nhap = fields.Selection(
        string='Mức thu nhập',
        selection=[('duoi_10', 'Dưới 10 triệu'),
                   ('tu_10_den_50', 'Từ 10 đến 50 triệu'),
                   ('tren_50', 'Trên 50 triệu'),
                   ], required=False, )
    so_nv = fields.Integer(string='Số nhân viên')
    ky_nang = fields.Char(string='Kỹ năng')
    trinh_do = fields.Char(string='Trình độ chuyên môn')
    so_thich = fields.Char(string='Sở thích')
    status = fields.Char(string='Trạng thái', required=False)

    lien_he_ten = fields.Many2one('dgis.customer',string='Họ tên bố')
    lien_sdt = fields.Char(string='Số điện thoại')
    lien_email = fields.Char(string="Email")
    lien_dia_chi = fields.Char(string='Dịa chỉ')

    lien_he_ten_1 = fields.Many2one('dgis.customer', string='Họ tên mẹ')
    lien_sdt_1 = fields.Char(string='Số điện thoại')
    lien_email_1 = fields.Char(string="Email")
    lien_dia_chi_1 = fields.Char(string='Dịa chỉ')

    childs = fields.One2many( comodel_name='dgis.customer', inverse_name='lien_he_ten',string='Con', required=False)
    childs_1 = fields.One2many( comodel_name='dgis.customer', inverse_name='lien_he_ten_1',string='Con', required=False)

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Tài khoản Email nhận bản sinh trắc',
        default=lambda self: self.env.user)

    _sql_constraints = [
        ('unique_Custom_ID', 'unique(Custom_ID)', u'ID trùng, hãy thử lại!'),
    ]


    # Vân tay trái
    thumb_l = fields.Selection(string='Ngón cái', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )
    index_finger_l = fields.Selection(string='Ngón trỏ', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )
    middle_finger_l = fields.Selection(string='Ngón giữa', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )
    ring_finger_l = fields.Selection(string='Ngón áp út', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )
    little_finger_l = fields.Selection(string='Ngón út', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )

    # Vân tay phải
    thumb_r = fields.Selection(string='Ngón cái', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )
    index_finger_r = fields.Selection(string='Ngón trỏ', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )
    middle_finger_r = fields.Selection(string='Ngón giữa', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )
    ring_finger_r = fields.Selection(string='Ngón áp út', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )
    little_finger_r = fields.Selection(string='Ngón út', selection=[('c1', 'Whorl'), ('c2', 'Composite'), ('c3', 'Loop'), ('c4', 'Radial Loop'), ('c5', 'Arch'), ('c6', 'Tented Arch')], required=False, )




    def my_random_string(self,string_length=8):
        """Returns a random string of length string_length."""
        random = str(uuid.uuid4())  # Convert UUID format to a Python string.
        random = random.upper()  # Make all characters uppercase.
        random = random.replace("-", "")  # Remove the UUID '-'.
        return random[0:string_length]  # Return the random string.
    @api.model
    def create(self, vals):
        if vals.get('Custom_ID', 'New') == 'New':
            vals['Custom_ID'] = self.my_random_string(8)
        result = super(Customers, self).create(vals)
        # trang_thai = "Chưa gửi"
        return result

    @api.depends("ngay_sinh")
    def get_tuoi(self):
        for rec in self:
            d = datetime.now() - rec.ngay_sinh
            # print((d))
            if d.days > 5840:
                rec.tuoi=True
            else:
                rec.tuoi = False

    @api.model
    def _default_image(self):
        """read image and set it by default:"""
        image_path = get_module_resource('custom_water', 'static/src/img', 'male.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))

    image = fields.Binary(
        "", default=_default_image, attachment=True,
        help="This field holds the image used as photo for the student, limited to 1024x1024px.")

    @api.onchange('lien_he_ten')
    def get_lien_he(self):
        for rec in self:
            if rec.lien_he_ten.so_dien_thoai:
                rec.lien_sdt = rec.lien_he_ten.so_dien_thoai
            if rec.lien_he_ten.email:
                rec.lien_email = rec.lien_he_ten.email
            if rec.lien_he_ten.diachi:
                rec.lien_dia_chi = rec.lien_he_ten.diachi

    @api.onchange('lien_he_ten_1')
    def get_lien_he_1(self):
        for rec in self:
            if rec.lien_he_ten_1.so_dien_thoai:
                rec.lien_sdt_1 = rec.lien_he_ten_1.so_dien_thoai
            if rec.lien_he_ten_1.email:
                rec.lien_email_1 = rec.lien_he_ten_1.email
            if rec.lien_he_ten_1.diachi:
                rec.lien_dia_chi_1 = rec.lien_he_ten_1.diachi

    def get_file_phan_tich(self):
        for rec in self:
            rec.file_phan_tich = rec.env['ir.attachment'].search([['res_id', '=', rec.id],['res_model', '=', 'dgis.customer']], limit=1).datas
            rec.filename = rec.env['ir.attachment'].search([['res_id', '=', rec.id],['res_model', '=', 'dgis.customer']], limit=1).datas_fname

    @api.multi
    def action_quotation_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        print(self.ensure_one())
        ir_model_data = self.env['ir.model.data']
        # print(ir_model_data)
        try:
            template_id = ir_model_data.get_object_reference('dgis', 'email_template_customer')[1]
            # print(template_id)
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        # lang = self.env.context.get('lang')
        # template = template_id and self.env['mail.template'].browse(template_id)
        # if template and template.lang:
        #     lang = template._render_template(template.lang, 'sale.order', self.ids[0])
        ctx = {
            'default_model': 'dgis.customer',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

class Ir_Data(models.Model):

    _inherit = 'ir.attachment'

