# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - Product Fiscal Company',
    'version': '10.0.1.0.0',
    'category': 'CIS',
    'summary': 'Glue Module between CIS and product',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'fiscal_company_base',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/view_product_template.xml',
        'views/view_product_pricelist.xml',
        'views/view_product_pricelist_item.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/product_pricelist.xml',
        'demo/product_template.xml',
        'demo/product_product.xml',
        'demo/res_company.xml',
    ],
    'installable': True,
    'auto_install': True,
}
