
from odoo import http
from odoo.http import request
class CustomerForm(http.Controller):
    # mention class name
    @http.route(['/customer/form'], type='http', auth="public", website=True)
    # mention a url for redirection.
    # define the type of controller which in this case is ‘http’.
    # mention the authentication to be either public or user.
    def partner_form(self, **post): # create method. this will load the form webpage
        return request.render("create_partner_by_website.tmp_customer_form", {})

    @http.route(['/customer/form/submit'], type='http', auth="public", website=True)
    # next controller with url for submitting data from the form#
    def customer_form_submit(self, **post):
        partner = request.env['dgis.customer'].create({
            'Custom_ID': post.get('id'),
            'file_phan_tich': post.get('file'),
        })
        vals = {
            'partner': partner,
        }
        # inherited the model to pass the values to the model from the form
        return request.render("create_partner_by_website.tmp_customer_form_success", vals)
    # finally send a request to render the thank you page