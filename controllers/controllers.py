# -*- coding: utf-8 -*-
from odoo import http

# class CustomWater(http.Controller):
#     @http.route('/custom_water/custom_water/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_water/custom_water/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_water.listing', {
#             'root': '/custom_water/custom_water',
#             'objects': http.request.env['custom_water.custom_water'].search([]),
#         })

#     @http.route('/custom_water/custom_water/objects/<model("custom_water.custom_water"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_water.object', {
#             'object': obj
#         })