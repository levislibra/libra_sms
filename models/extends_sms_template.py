# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExtendsSmsTemplate(models.Model):
	_inherit = 'sms.template'
	_description = 'Plantilla de SMS'

	body_len = fields.Integer('Cantidad de caracteres', compute='_compute_body_len')
	body_len_text = fields.Char('Cantidad de caracteres en texto', compute='_compute_body_len')
	company_id = fields.Many2one('res.company', string='Empresa', index=True, default=lambda self: self.env.company)

	@api.onchange('body')
	def _compute_body_len(self):
		if self.body:
			body_len = len(self.body)
			self.body_len_text = str(body_len) + " caracteres de 160 como maximo."
			self.body_len = body_len