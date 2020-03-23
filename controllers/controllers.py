import base64

from odoo import http
from odoo.http import request


class CustomerForm(http.Controller):
    # mention class name
    @http.route(['/customer/form'], type='http', auth="public", website=True) # mention a url for redirection. # define the type of controller which in this case is ‘http’. # mention the authentication to be either public or user.
    def partner_form(self, **post): # create method. this will load the form webpage
        customers = http.request.env['dgis.customer']
        return request.render("dgis.tmp_customer_form", {
            'customers': customers.search([])
        })

    @http.route('/customer/form/submit', type='http', auth="public", website=True)
    def upload_files(self, **post):
        if post.get('attachment', False):
            Attachments = request.env['ir.attachment']
            name = post.get('attachment').filename
            file = post.get('attachment')
            customer_id = post.get('id')
            attachment = file.read()
            # print(request.env['ir.attachment'].res_id)
            list_id = request.env['ir.attachment'].sudo().search_read([], ['res_id'])
            # print(list_id)
            if customer_id in list_id:
                attachment_id = Attachments.sudo().write({
                    'name': name,
                    'datas_fname': name,
                    'res_name': name,
                    'type': 'binary',
                    'res_model': 'dgis.customer',
                    'res_id': customer_id,
                    'datas': base64.b64encode(attachment),
                })
                value = {
                    'file_phan_tich': attachment_id
                }
            else:
                attachment_id = Attachments.sudo().create({
                    'name': name,
                    'datas_fname': name,
                    'res_name': name,
                    'type': 'binary',
                    'res_model': 'dgis.customer',
                    'res_id': customer_id,
                    'datas': base64.b64encode(attachment),
                })
                value = {
                    'file_phan_tich': attachment_id
                }
        # print(type(attachment_id))
        return request.render("dgis.tmp_customer_form_success", value)
