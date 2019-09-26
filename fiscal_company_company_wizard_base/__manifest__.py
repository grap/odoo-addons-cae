# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - Company Wizard - Base',
    'version': '12.0.1.0.0',
    'category': 'CAE',
    'summary': 'Glue Module between CAE and Company Wizard - Base modules',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'fiscal_company_base',
        'company_wizard_base',
    ],
    'data': [
        'views/view_res_company_create_wizard.xml',
    ],
    'installable': True,
    'auto_install': True,
}
