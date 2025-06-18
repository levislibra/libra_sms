# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ExtendsSmsSms(models.Model):
	_inherit = 'sms.sms'
	_description = 'Mensaje de texto'

	name = fields.Char("Nombre")
	template_id = fields.Many2one('sms.template', string='Plantilla', domain="[('model_id', '=', 'res.partner')]")
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
			self.template_id = False
			self.body = ''

	# constraint: body length must be less than or equal to 160 characters
	@api.constrains('body')
	def _check_body_length(self):
		for record in self:
			if record.body and len(record.body) > 160:
				raise ValidationError(_("El cuerpo del mensaje no puede tener más de 160 caracteres."))

	@api.onchange('template_id')
	def _onchange_template_id(self):
		if self.template_id:
			self.body = self.template_id._render_field(
				'body', [self.partner_id.id],
				compute_lang=True
			)[self.partner_id.id]
		else:
			self.body = ''
			

class ExtendsSmsComposer(models.TransientModel):
	_inherit = 'sms.composer'

	# constraint: body length must be less than or equal to 160 characters
	@api.constrains('body')
	def _check_body_length(self):
		for record in self:
			if record.body and len(record.body) > 160:
				raise ValidationError(_("El cuerpo del mensaje no puede tener más de 160 caracteres."))