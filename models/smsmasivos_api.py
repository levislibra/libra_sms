# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, models
from odoo.addons.iap.tools import iap_tools
import requests

DEFAULT_ENDPOINT = 'https://iap-sms.odoo.com'

URL_ENVIAR_SMS = 'http://servicio.smsmasivos.com.ar/enviar_sms.asp?api=1'

URL_ENVIAR_BLOQUE = 'http://servicio.smsmasivos.com.ar/enviar_sms_bloque.asp'

class ExtendsSmsApi(models.AbstractModel):
	_inherit = 'sms.api'
	_description = 'SMS API - SMS Masivos'

	@api.model
	def _send_sms_batch(self, messages, company_id):
		""" Send SMS using IAP in batch mode

		:param messages: list of SMS to send, structured as dict [{
			'res_id':  integer: ID of sms.sms,
			'number':  string: E164 formatted phone number,
			'content': string: content to send
		}]
		:return: return of /iap/sms/1/send controller which is a list of dict [{
			'res_id': integer: ID of sms.sms,
			'state':  string: 'insufficient_credit' or 'wrong_number_format' or 'success',
			'credit': integer: number of credits spent to send this SMS,
		}]
		:raises: normally none
		"""
		params = {
			'usuario': company_id.usuario,
			'clave': company_id.password,
			'bloque': messages,
		}
		r = requests.get(URL_ENVIAR_BLOQUE, params=params)
		return r

	@api.model
	def _send_sms(self, res_id, number, content, company_id):
		""" Send SMS using IAP in batch mode

		:param messages: list of SMS to send, structured as dict [{
			'res_id':  integer: ID of sms.sms,
			'number':  string: E164 formatted phone number,
			'content': string: content to send
		}]
		:return: return of /iap/sms/1/send controller which is a list of dict [{
			'res_id': integer: ID of sms.sms,
			'state':  string: 'insufficient_credit' or 'wrong_number_format' or 'success',
			'credit': integer: number of credits spent to send this SMS,
		}]
		:raises: normally none
		"""

		params = {
			'usuario': company_id.usuario,
			'clave': company_id.password,
			'tos': self._sanitize_phone_number(number, company_id.country_id),
			'texto': content,
			'respuestanumerica': 1,
			'idinterno': str(res_id),
		}
		r = requests.get(URL_ENVIAR_SMS, params=params)
		return r

	@api.model
	def _sanitize_phone_number(self, number, country_id):
		ret = number
		if country_id.name in ['Argentina','México','Colombia']:
			if len(number) > 10:
				ret = number[len(number)-10:]
		if country_id.name == 'Perú':
			if len(number) > 9:
				ret = number.replace('+51', '').replace(' ', '')
		return ret

	@api.model
	def _process_status(self, text, model_id):
		resultado = text.split(';')
		if len(resultado) > 1:
			status = int(resultado[0])
			model_id.status = resultado[0]
			if status == 0:
				model_id.state = 'sent'
			if status == 1:
				model_id.state = 'canceled'
			if status <= -1:
				model_id.state = 'error'
			detalle = resultado[1].split(".")
			error_message = detalle[0]
			model_id.error_message = error_message
