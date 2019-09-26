# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - Account',
    'version': '12.0.1.0.0',
    'category': 'CAE',
    'summary': 'Glue Module between CAE and Account modules',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'fiscal_company_base',
        'account',
    ],
    'data': [
        'security/ir_rule.xml',
        'views/menu.xml',
        'views/view_account_journal.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/account_account.xml',
        'demo/account_journal.xml',
        'demo/account_tax.xml',
        'demo/product_category.xml',
        'demo/product_product.xml',
        'demo/product_template.xml',
        'demo/res_partner.xml',
        'demo/ir_property.xml',
    ],
    'installable': True,
    'auto_install': True,
}
