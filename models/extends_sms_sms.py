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

	@api.onchange('body')
	def _compute_body_len(self):
		if self.body:
			body_len = len(self.body)
			self.body_len_text = str(body_len) + " caracteres de 160 como maximo."
			self.body_len = body_len

	# def _send(self, unlink_failed=False, unlink_sent=True, raise_exception=False):
	# 	""" This method tries to send SMS after checking the number (presence and
	# 	formatting). """
	# 	# get str format record.id,record.number,record.body\n from self
	# 	iap_data = "\n".join(["%s,%s,%s" % (record.id, record.number, record.body) for record in self])
	# 	iap_results = self.env['sms.api']._send_sms_batch(iap_data, self.company_id)
	# 	print("iap_results", iap_results)
	# 	print("iap_results", iap_results.text)
	# 	if iap_results.status_code != 200:
	# 		raise ValidationError("Error: " + iap_results.text)
		# except Exception as e:
		# 	_logger.info('Sent batch %s SMS: %s: failed with exception %s', len(self.ids), self.ids, e)
		# 	if raise_exception:
		# 		raise
		# 	self._postprocess_iap_sent_sms(
		# 		[{'res_id': sms.id, 'state': 'server_error'} for sms in self],
		# 		unlink_failed=unlink_failed, unlink_sent=unlink_sent)
		# else:
		# 	_logger.info('Send batch %s SMS: %s: gave %s', len(self.ids), self.ids, iap_results)
		# 	self._postprocess_iap_sent_sms(iap_results, unlink_failed=unlink_failed, unlink_sent=unlink_sent)


# class LibraSms(models.Model):
# 	_name = 'libra.sms'
# 	_description = 'Mensaje de texto'

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