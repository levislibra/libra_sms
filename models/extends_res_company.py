# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta

class ExtendsResCompany(models.Model):
	_inherit = 'res.company'

	contracted_module = fields.Boolean(string='Módulo contratado', default=False)
	usuario = fields.Char('Usuario')
	password = fields.Char('Clave')
	
