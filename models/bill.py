from odoo import fields, models, api


class Bill(models.Model):
    _name = 'cmsw.bill'
    _description = 'Description'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _inherit = {'cmsw.amount_of_water': 'amount_of_water_id'}
    _rec_name = 'number'

    currency_id = fields.Many2one('res.currency', string='Currency', help="Main currency of the company.", default=lambda self: self.env['res.currency'].search([('name','=','VND')]))

    # name = fields.Char(string='Name Order', required=True, copy=False, readonly=True,
    #                    states={'draft': [('readonly', False)]},
    #                    index=True, default=lambda self: _('New'))

    #=======botom=======
    amount_untax = fields.Monetary( string='Tiền nước', store=True, readonly=True, compute='_tinh_tong_tien', )
    tax_env = fields.Monetary(string='Thuế bảo vệ môi trường (10%)', required=False, store=True, readonly=True, compute='_tinh_tong_tien')
    tax_vat = fields.Monetary(string='Thuế VAT (5%)', required=False, store=True, readonly=True, compute='_tinh_tong_tien')
    amount_total = fields.Monetary(string='Tổng tiền', required=False, store=True, readonly=True, compute='_tinh_tong_tien')

    amount_of_water_line = fields.One2many(
        comodel_name='cmsw.amount_of_water', compute='print_amount_of_water_line',
        inverse_name='bill_id',
        string='Số nước',
        required=False)
    # amount_of_water_line = fields.Many2one(
    #     comodel_name='cmsw.amount_of_water', compute='print_amount_of_water_line',
    #     string='Số nước',
    #     required=False)

    #==== header ========
    company_id = fields.Many2one(string='Đơn vị cấp nước ', comodel_name='res.company')
    code = fields.Char(string='Mãu số', required=False)
    sign = fields.Char(string='Kí hiệu', required=False)
    number = fields.Char(string='Số(TT)', required=False, copy=False, readonly=True,
                         index=True, default=lambda self: ('New'))
    tax_code = fields.Char(string='Mã số thuế', required=False)
    month = fields.Integer(string='Tháng sử dụng', required=False)
    from_date = fields.Date(string='Từ ngày', required=True)
    to_date = fields.Date(string='Đến ngày', required=True)
    create_at_bill = fields.Datetime(string='Ngày xuất hóa đơn', required=True, default=fields.Datetime.now)
    create_at_water = fields.Date(string='Ngày ghi số nước', required=True)

    # === Name and address====
    customer_id = fields.Char(
        string='Mã khách hàng',
        required=False)
    household_id = fields.Many2one(
        comodel_name='cmsw.household',
        string='Tên khách hàng',
        required=True)
    apart_num = fields.Char(string='Số nhà', required=True,)
    street = fields.Char(string='Tổ/Xóm', required=True,)
    town = fields.Char(string='Phường/Xã', required=True,)
    province = fields.Char(string='Tỉnh', required=True,)
    district = fields.Char(string='Huyện', required=True,)
    note = fields.Text(string='Address', required=True, compute='_doc_tong_tien')

    @api.model
    def create(self, vals):
        if vals.get('number', ('New')) == ('New'):
            if 'company_id' in vals:
                vals['number'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'cmsw.bill') or ('New')
            else:
                vals['number'] = self.env['ir.sequence'].next_by_code('cmsw.bill') or ('New')
        result = super(Bill, self).create(vals)
        return result

    @api.depends("month", "household_id")
    @api.multi
    def print_amount_of_water_line(self):
        for rec in self:
            rec.amount_of_water_line = self.env['cmsw.amount_of_water'].search([['household_id', '=', rec.household_id.id], ['month', '=', rec.month]])
            print("==============++++++++++++++++")
            #print(self.household_id.amount_water_id)
        return {'domain': {'household_id': ['id', 'in', rec.amount_of_water_line]}}

    @api.depends("amount_of_water_line.price_subtotal")
    def _tinh_tong_tien(self):
        for rec in self:
            amount_total = amount_untax = tax_env = tax_vat = 0
            for line in rec.amount_of_water_line:
                amount_untax += line.price_subtotal
            tax_env = (amount_untax*10)/100
            tax_vat = (amount_untax*5)/100
            amount_total = amount_untax + tax_env + tax_vat

            rec.update({
                'amount_untax': amount_untax,
                'tax_env': tax_env,
                'tax_vat': tax_vat,
                'amount_total': amount_total,
            })

    @api.onchange('household_id')
    @api.multi
    def _onchange_address(self):
        if self.household_id.apart_num:
            self.apart_num = self.household_id.apart_num
        if self.household_id.street:
            self.street = self.household_id.street
        if self.household_id.address_id:
            self.town = self.household_id.address_id.town
        if self.household_id.address_id.province:
            self.province = self.household_id.address_id.province
        if self.household_id.address_id.district:
            self.district = self.household_id.address_id.district
        if self.household_id.name_seq:
            self.customer_id = self.household_id.name_seq
        if self.household_id.tax_id:
            self.tax_code = self.household_id.tax_id

    @api.onchange("amount_of_water_line")
    def _onchange_date(self):
        for rec in self:
            for line in rec.amount_of_water_line:
                self.from_date = line.from_date
                self.to_date = line.to_date
                self.create_at_water = line.create_at

    @api.depends("amount_total")
    def _doc_tong_tien(self):
        # self.note = "aaa"
        amount = int(self.amount_total)
        self.note = (self.num2words(amount)+" đồng").upper()

    def num2words(self,num):
        under_20 = ['không', "một", "hai ", "ba ", "bốn ", "năm ", "sáu ", "bảy ", "tám ", "chín ", "mười ",
                    "mười một ", "mười hai ", "mười ba ", "mười bốn ", "mười lăm ", "mười sáu ", "mười bảy ", "mười tám ", "mười chín "]
        tens = ["hai mươi ", "ba mươi ", "bốn mươi ", "năm mươi ", "sáu mươi ", "bảy mươi ", "tám mươi ", "chín mươi "]
        above_100 = {100: 'trăm', 1000: 'nghìn', 1000000: 'triệu', 1000000000: 'tỉ'}
        vn = ['mốt','lăm']

        if num < 20:
            return under_20[num]

        if num < 100:
            return tens[(int)(num / 10) - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

        # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
        pivot = max([key for key in above_100.keys() if key <= num])

        return self.num2words((int)(num / pivot)) + ' ' + above_100[pivot] + (
            '' if num % pivot == 0 else ' ' + self.num2words(num % pivot))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='draft')
    @api.multi
    def action_cancel(self):
        # self.mapped('picking_ids').action_cancel()
        return self.write({'state': 'cancel'})

    @api.multi
    def action_done(self):
        return self.write({'state': 'done'})

    @api.multi
    def action_draft(self):
        # orders = self.filtered(lambda s: s.state in ['cancel', 'sent'])
        # return orders.write({
        #     'state': 'draft',
        # })
        return self.write({'state': 'done'})
    # print quotation
    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'done'})
        return self.env.ref('custom_water.bill_basic_report') \
            .with_context({'discard_logo_check': True}).report_action(self)

class Company(models.Model):

    _inherit = 'res.company'
    _description = ''

    signature = fields.Binary(string='Chữ ký', attachment=True,)