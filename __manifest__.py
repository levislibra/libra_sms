# -*- coding: utf-8 -*-
{
    'name': "Libra SMS",

    'summary': """
        SMS module for Libra Lending""",

    'description': """
        SMS module for Libra Lending
    """,

    'author': "Librasoft SAS",
    'website': "https://www.libra-soft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
	'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','libra_base_automation','mail','libra_lending','sms'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/sms_template.xml',
        'views/sms.xml',
		'views/sms_automation.xml',
		'views/extends_res_company.xml',
    ],
    'assets': {
		'web.assets_backend': [
			'libra_sms/static/src/css/hide_sms_link.css',
		],
	},
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
