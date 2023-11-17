# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ExtendsBaseAutomation(models.Model):
	_inherit = 'base.automation'


	def sms_action_review(self):
		self.status = 'review'
		self.active = False
		template = self.env.ref('libra_sms.mail_base_automation_sms_review')
		template.send_mail(self.id, force_send=True)

	def sms_action_approved(self):
		self.status = 'approved'
		self.active = True

	def sms_action_draft(self):
		self.status = 'draft'
		self.active = False