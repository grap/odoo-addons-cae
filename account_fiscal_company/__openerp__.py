# coding: utf-8
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - Account',
    'version': '10.0.1.0.0',
    'category': 'CAE',
    'summary': 'Manage Cooperatives of Activities and Employment - Account',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'account',
    ],
    'data': [
        'security/ir_rule.xml',
#        'security/ir.model.access.csv',
#        'view/account_view.xml',
#        'view/account_invoice_view.xml',
#        'view/view.xml',
        'views/view_res_company_create_wizard.xml'
    ],
    'demo': [
        'demo/res_groups.xml',
#        'demo/account_fiscalyear.xml',
#        'demo/account_period.xml',
        'demo/account_account.xml',
        'demo/account_journal.xml',
        'demo/ir_property.xml',
    ],
    'installable': True,
    'auto_install': True,
}
