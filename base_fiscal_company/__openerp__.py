# coding: utf-8
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - Base',
    'version': '10.0.1.0.0',
    'category': 'CAE',
    'summary': 'Manage Cooperatives of Activities and Employment',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/res_groups.xml',
        'views/action.xml',
        'views/menu.xml',
        'views/view_res_users.xml',
        'views/view_res_partner.xml',
        'views/view_res_company.xml',
        'views/view_res_company_create_wizard.xml',
    ],
    'demo': [
        'demo/res_partner_company.xml',
        'demo/res_partner_users.xml',
    ],
    'installable': True,
}
