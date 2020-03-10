
from odoo import api, fields, models

class User(models.Model):

    _inherit = 'res.users'
    _description = ''

    # employee_ids = fields.One2many('hr.employee', 'user_id', string='Related employees')
    name = fields.Char(string='Họ tên ')
    login = fields.Char( string='Địa chỉ Email')
    phone = fields.Char( string='Số điện thoại')
    address_id = fields.Many2many( comodel_name='cmsw.address', string='Khu vực quản lý')
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Nhân viên',
        readonly=True)
    function = fields.Selection(
        string='Chức vụ',
        selection=[ ('admin', 'Admin'),
                    ('ql', 'Quản lý'),
                    ('nvkv', 'Nhân viên khu vực'),
                    ('nvnl', 'Nhân viên nhập liệu '),
                    ], required=False,)

    # @api.onchange("employee_id")
    # def get_account_partner(self):
    #     for a in self:
    #         for rec in a.employee_ids:
    #             if rec.employee_id.name:
    #                 rec.name = rec.employee_id.name
    #             if rec.employee_id.mobile_phone:
    #                 rec.phone = rec.employee_id.mobile_phone
    #             if rec.employee_id.work_email:
    #                 rec.login = rec.employee_id.work_email
    #             if rec.employee_id.function:
    #                 rec.function = rec.employee_id.function


class Parner(models.Model):

    _inherit = 'hr.employee'
    _translate = True

    function = fields.Selection(
        string='Chức vụ',
        selection=[('admin', 'Admin'),
                   ('ql', 'Quản lý'),
                   ('nvkv', 'Nhân viên khu vực'),
                   ('nvnl', 'Nhân viên nhập liệu '),
                   ], required=False)
