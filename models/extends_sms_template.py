# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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

	# constraint: body length must be less than or equal to 160 characters
	@api.constrains('body')
	def _check_body_length(self):
		for record in self:
			if record.body and len(record.body) > 160:
				raise ValidationError(_("El cuerpo del mensaje no puede tener más de 160 caracteres."))