# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - CRM Fiscal Company',
    'version': '10.0.1.0.0',
    'category': 'CAE',
    'summary': 'Glue Module between CAE and CRM modules',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'fiscal_company_base',
        'crm',
    ],
    'data': [
        'security/ir_rule.xml',
        'views/view_crm_activity.xml',
        'views/view_crm_lead.xml',
        'views/view_crm_lead_tag.xml',
        'views/view_crm_lost_reason.xml',
        'views/view_crm_stage.xml',
    ],
    'installable': False,
    'auto_install': True,
}
