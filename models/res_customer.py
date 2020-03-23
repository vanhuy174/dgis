import base64
import os
import random
import uuid
from odoo.modules.module import get_module_resource
from odoo import tools
from odoo import api, fields, models


class Customers(models.Model):
    _name = 'dgis.customer'
    _inherit = 'res.partner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = ''
    _rec_name = 'ho_ten'

    is_form = fields.Boolean(string='Form nhập', default=False)
    Custom_ID = fields.Char(string='ID', readonly=True, store=True)
    image_dgis = fields.Binary(
        "File vân tay", attachment=True, )
    file_phan_tich = fields.Binary(
        "File sau phân tích ", attachment=True, )
    ho_ten = fields.Char(string='Họ tên', required=True, )
    email = fields.Char(string='Địa chỉ Email', required=True, )
    so_dien_thoai = fields.Char(string='Số điện thoại', required=True)
    gioi_tinh = fields.Selection(
        string='Giới tính',
        selection=[('nam', 'Nam'),
                   ('nu', 'Nữ'),
                   ], required=False, )
    ngay_sinh = fields.Date(string='Ngày sinh')
    cmnd = fields.Char(string='Số CMND')
    diachi = fields.Char(string='Địa chỉ', required=True)
    nghe_nghiep = fields.Char(string='Nghề Nghiệp')
    tt_honnhan = fields.Selection(string='Tình trạng hôn nhân',
                                  selection=[('dt', 'Độc thân'),
                                             ('dkh', 'Đã kết hôn'),
                                             ('dlh', 'Đã ly hôn'),
                                             ], required=False, )
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
    lien_he_ten = fields.Many2one('dgis.customer', string='Họ tên')
    lien_sdt = fields.Char(string='Số điện thoại')
    lien_email = fields.Char(string="Email")
    lien_dia_chi = fields.Char(string='Dịa chỉ')

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Tài khoản Email nhận bản sinh trắc',
        default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        seq_obj = self.env['ir.sequence']
        vals['Custom_ID'] = seq_obj.next_by_code('dgis.customer.service')
        return super(Customers, self).create(vals)

    # def my_random_string(self,string_length=8):
    #     """Returns a random string of length string_length."""
    #     random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    #     random = random.upper()  # Make all characters uppercase.
    #     random = random.replace("-", "")  # Remove the UUID '-'.
    #     return random[0:string_length]  # Return the random string.
    #
    # def get_id(self):
    #     temp = False
    #     for rec in self:
    #         # print(type(rec.Custom_ID))
    #         if rec.Custom_ID == False and temp == False:
    #             if temp == True:
    #                 break
    #             rec.Custom_ID = rec.my_random_string(8)
    #             temp = True

    # if rec.Custom_ID != None:
    #     rec.Custom_ID = True
    #     temp == True
    # if temp == True or rec.Custom_ID != False:
    #     break

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

    @api.multi
    def action_send_to_infolife(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('DGIS', 'email_template_customer')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        print(template_id, compose_form_id)
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


