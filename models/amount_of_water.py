from odoo import models, fields, api

class AmountOfWater(models.Model):
    _name = 'cmsw.amount_of_water'
    _description = 'Số nước'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'month'


    currency_id = fields.Many2one('res.currency', string='Currency', help="Main currency of the company.", default=lambda self: self.env['res.currency'].search([('name','=','VND')]))
    month = fields.Integer( string='Tháng',required=False)
    from_date = fields.Date( string='Từ ngày', required=False)
    to_date = fields.Date( string='Đến ngày ', required=False)
    csc = fields.Integer( string='Chỉ số cũ ', required=False, )
    csm = fields.Integer( string='Chỉ số mới', required=False)
    consume = fields.Integer( string='Tổng tiêu thụ', compute='_tinh_tieu_thu', store=True)
    price = fields.Integer( string='Đơn giá/m3 ', required=False, compute='_tinh_don_gia')
    create_at = fields.Date(string='Ngày ghi số nước', required=False)
    update_at = fields.Date( string='Thời gian cập nhập', required=False)
    price_subtotal = fields.Monetary( string='Thành tiền', required=False, compute='_tinh_thanh_tien', store=True)
    household_id = fields.Many2one( comodel_name='cmsw.household', string='Hộ gia đình', required=False)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        required=False)
    bill_id = fields.Many2one(
        comodel_name='cmsw.bill',
        string='Hóa đơn',
        required=False)

    @api.depends("csc", "csm")
    def _tinh_tieu_thu(self):
        for rec in self:
            rec.consume = rec.csm - rec.csc

    @api.depends('household_id.area','household_id.pur_use')
    def _tinh_don_gia(self):
        for rec in self:
            if rec.household_id.area == 'vip':
                if rec.household_id.pur_use == 'SH': rec.price = 8400
                elif rec.household_id.pur_use == 'SX': rec.price = 14000
                elif rec.household_id.pur_use == 'DV': rec.price = 18000
                else: rec.price = 14000
            if rec.household_id.area == 'normal':
                if rec.household_id.pur_use == 'SH': rec.price = 8300
                elif rec.household_id.pur_use == 'SX': rec.price = 14000
                elif rec.household_id.pur_use == 'DV': rec.price = 15000
                else: rec.price = 14000
            if rec.household_id.area == 'hard':
                if rec.household_id.pur_use == 'SH': rec.price = 8200
                elif rec.household_id.pur_use == 'SX': rec.price = 14000
                elif rec.household_id.pur_use == 'DV': rec.price = 15000
                else: rec.price = 14000

    @api.depends("consume", "price")
    def _tinh_thanh_tien(self):
        for rec in self:
            rec.price_subtotal = rec.consume * rec.price

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
    # @api.depends("csm", "month")
    # def _tinh_chi_so_cu(self):
    #     self._cr.execute("SELECT month FROM cmsw_amount_of_water ")
    #     data = self._cr.fetchall()
    #     for rec in self:
    #         print(rec.month)
    #         break;
        #print(self[1].month)
            #for i in range(rec[0].month):
            #     print(i)
            #     break

            # for i in range(len(data)-1):
            #     j=i+1
            #     for j in range(len(data)):
                    #if (data[j]>data[i]) and self.month[j]-self.month[i]==1:
                #     self.csc = self.csm

        #     if (data[i]-data[i-1])==1:
        #          self.csc = self.csm
        # print("=========+++++++++++++++")




    # @api.onchanges('household_id.area', 'household_id.pur_use')
    # def _update_don_gia(self):
    #     return self._tinh_don_gia