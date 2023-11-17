# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExtendsSmsTemplate(models.Model):
	_inherit = 'sms.template'
	_description = 'Plantilla de SMS'

	company_id = fields.Many2one('res.company', string='Empresa', index=True, default=lambda self: self.env.company)

