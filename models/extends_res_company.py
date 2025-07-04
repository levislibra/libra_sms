# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta

class ExtendsResCompany(models.Model):
	_inherit = 'res.company'

	sms_usuario = fields.Char('Usuario')
	sms_password = fields.Char('Clave')

