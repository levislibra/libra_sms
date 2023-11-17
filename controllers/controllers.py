# -*- coding: utf-8 -*-
# from odoo import http


# class LibraSms(http.Controller):
#     @http.route('/libra_sms/libra_sms', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/libra_sms/libra_sms/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('libra_sms.listing', {
#             'root': '/libra_sms/libra_sms',
#             'objects': http.request.env['libra_sms.libra_sms'].search([]),
#         })

#     @http.route('/libra_sms/libra_sms/objects/<model("libra_sms.libra_sms"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('libra_sms.object', {
#             'object': obj
#         })
