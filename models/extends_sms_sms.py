# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class ExtendsSmsSms(models.Model):
	_inherit = 'sms.sms'
	_description = 'Mensaje de texto'

	name = fields.Char()
	body = fields.Text()
	body_len = fields.Integer('Cantidad de caracteres', compute='_compute_body_len')
	body_len_text = fields.Char('Cantidad de caracteres en texto', compute='_compute_body_len')
	error_message = fields.Char("Mensaje de error")
	status = fields.Char("Estado")
	company_id = fields.Many2one('res.company', string='Empresa', index=True, default=lambda self: self.env.company)

	@api.model_create_multi
	def create(self, vals_list):
		results = super(ExtendsSmsSms, self).create(vals_list)
		for res in results:
			res.name = 'MSJ/' + str(res.id).zfill(10)
		return results

	def _send(self, unlink_failed=False, unlink_sent=True, raise_exception=False):
		""" This method tries to send SMS after checking the number (presence and
		formatting). """
		for record in self:
			r = self.env['sms.api']._send_sms(record.id, record.number, record.body, record.company_id)
			if r.status_code == 200:
				self.env['sms.api']._process_status(r.text, record)

	@api.onchange('partner_id')
	def _onchange_partner_id(self):
		if self.partner_id:
			self.number = self.partner_id.mobile

	@api.onchange('body')
	def _compute_body_len(self):
		if self.body:
			body_len = len(self.body)
			self.body_len_text = str(body_len) + " caracteres de 160 como maximo."
			self.body_len = body_len

class ExtendsSmsComposer(models.TransientModel):
	_inherit = 'sms.composer'

	body_len = fields.Integer('Cantidad de caracteres', compute='_compute_body_len')
	body_len_text = fields.Char('Cantidad de caracteres en texto', compute='_compute_body_len')

	@api.onchange('body')
	def _compute_body_len(self):
		if self.body:
			body_len = len(self.body)
			self.body_len_text = str(body_len) + " caracteres de 160 como maximo."
			self.body_len = body_len