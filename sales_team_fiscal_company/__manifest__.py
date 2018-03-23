# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - Sales Team Fiscal Company',
    'version': '10.0.1.0.0',
    'category': 'CAE',
    'summary': 'Glue Module between CAE and Sales Team modules',
    'description': """
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'sales_team',
    ],
    'data': [
        'views/view_crm_team.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
    'installable': False,
    'auto_install': False,
}
