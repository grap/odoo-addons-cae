# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CIS - Product Fiscal Company',
    'version': '8.0.5.0.0',
    'category': 'CIS',
    'summary': 'Glue Module between CIS and product',
    'description': """
Glue Module between CIS and product
===================================

Features
--------

* 'company_id' is now mandatory on 'product.product' model;
* 'company_id' is now mandatory on 'product.pricelist' model;

* user in mother company can see product of all child company;
* user in fiscal company can see but not update / delete product
  of mother company;
* Add a field 'is_administrative' on product.product; if checked the
  product will not be updatable by basic users;

Company Creation Wizard
-----------------------

* Create a Sale Pricelist and the according property to
  property_product_pricelist;

Technical Information
---------------------

* After installing this module, please fill correctly the new required
  company_field;

Copyright, Author and Licence
-----------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'product',
    ],
    'data': [
        'security/ir_rule.xml',
        'data/ir_sequence_type.xml',
        'views/view_product_template.xml',
        'views/product_product_view.xml',
        'views/product_pricelist_view.xml',
        'views/product_pricelist_version_view.xml',
        'views/product_pricelist_item_view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/product_pricelist.xml',
        'demo/product_pricelist.yml',
        'demo/product_pricelist_version.yml',
        'demo/product_product.yml',
        'demo/function.xml',
    ],
    'installable': True,
    'auto_install': True,
}
