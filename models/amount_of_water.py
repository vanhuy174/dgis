from odoo import models, fields, api, exceptions

class AmountOfWater(models.Model):
    _name = 'cmsw.amount_of_water'
    _description = 'Số nước'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'month'


    currency_id = fields.Many2one('res.currency', string='Currency', help="Main currency of the company.", default=lambda self: self.env['res.currency'].search([('name','=','VND')]))
    month = fields.Integer( string='Tháng',required=False)
    from_date = fields.Date( string='Từ ngày', required=False)
    to_date = fields.Date( string='Đến ngày ', required=False)
    csc = fields.Integer( string='Chỉ số cũ ', required=False, readonly=True, compute='_tinh_csc', store = True)
    csm = fields.Integer( string='Chỉ số mới', required=False)
    consume = fields.Integer( string='Tiêu thụ', compute='_tinh_tieu_thu', store=True)
    average = fields.Float()

    price = fields.Monetary( string='Đơn giá/m3 ', required=False, compute='_tinh_don_gia', store=True)
    create_at = fields.Date(string='Ngày ghi số nước', required=False)
    update_at = fields.Date( string='Thời gian cập nhập', required=False)
    price_subtotal = fields.Monetary( string='Thành tiền', required=False, compute='_tinh_thanh_tien', store=True)
    household_id = fields.Many2one( comodel_name='cmsw.household', string='Hộ gia đình', required=False, )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Người cập nhập',
        required=False,
        compute="_auto_load_user_import")
    bill_id = fields.Many2one(
        comodel_name='cmsw.bill',
        string='Hóa đơn',
        required=False)

    @api.depends("csc", "csm")
    def _tinh_tieu_thu(self):
        for rec in self:
            rec.consume = rec.csm - rec.csc

    @api.depends("user_id")
    def _auto_load_user_import(self):
        for rec in self:
            for line in rec.household_id.address_id.user_id:
                if line.function == "nvnl":
                    rec.user_id = line.id

    @api.depends("csc", "csm")
    def _canh_bao_nuoc(self):
        for rec in self:
            for line in rec.household_id:
                print(line)

    # @api.constrains("consume")  # bắt ngoại lệ khi nhập số lượng
    # def _canh_bao_nuoc(self):
    #     for rec in self:
    #         average = 0.0
    #         total = 0
    #         count = 0
    #         for line in rec.household_id.amount_water_id:
    #             count += 1
    #             total += line.consume
    #             average = total/ count
    #             temp = rec.consume - average
    #             if temp > 50:
    #                 raise exceptions.ValidationError(u"Lượng nước tiêu thụ tăng đột biến!")

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

    @api.depends('household_id')
    def _tinh_csc(self):
        for rec in self:
            if rec.household_id:
                sql = "SELECT MAX(csm) FROM cmsw_amount_of_water WHERE household_id = %d ;" % rec.household_id.id
                self.env.cr.execute(sql)
                data = self.env.cr.fetchall()
                rec.csc = data[0][0]
                if rec.csc == rec.csm and data[0][0] != None:
                    sql = "SELECT MAX( csm ) FROM cmsw_amount_of_water WHERE csm < %d AND household_id = %d ;" %(data[0][0], rec.household_id.id)
                    self.env.cr.execute(sql)
                    csc = self.env.cr.fetchall()
                    rec.csc = csc[0][0]


    # @api.depends('csm','month','household_id')
    # def _tinh_csc(self):
    #     sql = "SELECT household_id, COUNT(*) FROM cmsw_amount_of_water GROUP BY household_id;"
    #     self.env.cr.execute(sql)
    #     household = self.env.cr.fetchall()
    #     # print(household)
    #     for i in range(len(household)):
    #         for j in range(household[i][1]):
    #             for rec in self:
    #                 if rec.household_id.id == household[i][0]:
    #                     sql1 = "SELECT csm FROM cmsw_amount_of_water WHERE household_id = %d GROUP BY csm ;" % rec.household_id.id
    #                     rec.env.cr.execute(sql1)
    #                     data = rec.env.cr.fetchall()
    #                     #print(data)
    #                     for n in range(len(data)):
    #                         #print(n)
    #                         if n==0:
    #                             rec.csc = 0
    #                         elif n < len(data)-1:
    #                             #rec.csc = data[n+1][0]
    #                             print(data[n+1][0])
    #                         else:
    #                             break
                                #print((data[0][n+1]))
                        # print((rec.csm))
                    #break
                break
           # break
    #
    # @api.depends('csm','month','household_id')
    # def _get_csc(self):
    #     for rec in self:
    #         rec.csc = self._tinh_csc()
    # @api.depends('csm','month','household_id')
    # def _tinh_csc(self, household=None):
    #     #sql = "select amount_water_id_month, MAX(amount_water_id_csm) from cmsw_household group by amount_water_id_month;"
    #     #sql = "SELECT household_id, month, COUNT(*) FROM cmsw_amount_of_water GROUP BY household_id, month;"
    #     sql = "SELECT household_id,month,csc, csm FROM cmsw_amount_of_water GROUP BY household_id, month, csc, csm;"
    #     self.env.cr.execute(sql)
    #     months = self.env.cr.fetchall()
    #     print(months)
    #     c = 0
    #     for i in range(len(months)):
    #         for a in self:
    #             if a.household_id.id == months[i][0]:
    #                 for rec in a.household_id:
    #                     for j in rec.amount_water_id:
    #                         j.household_id.groupby('household_id')
    #                         if i==0:
    #                             j.csc = 0
    #                         # j.csc = j.csm
    #                         # print(len(months))
    #                         if i > 0:
    #                             l = list(months[i-1])
    #                             l2 = list(months[i])
    #                             if a.household_id.id == l2[0]:
    #                                 # print(l[1]- l2[1])
    #                                 # if l[1] - l2[1] == 0 :
    #                                 #     l2[2] = 0
    #                                 #     j.csc = l2[2]
    #                                 if l[1] - l2[1] == 1 or l2[1] - l[1] == -11:
    #                                     # j.csc = l2[2]
    #                                     l[2] = l2[3]
    #                                     # j.csc = l2[2]
    #                                     # print("==============================================")
    #                                     # print(l[1] - l2[1])
    #                                     print(l[2])
                            # print(l2[1]-l[1])
                            # if i==0:
                            #     j.csc=0
                            # if months[i][1]-months[i-1][1]==1:


                            # c +=1
                #             break
                #         break
                #     break
                # break
            # break
        # return res_all

