# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Account Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'CIS - Account Fiscal Company',
    'version': '1.1',
    'category': 'CIS',
    'description': """
Manage specific account move for cooperative
============================================

Features :
----------
* Create a field res_company.fiscal_company:
    * This field allow user to create account move in a company, but with
      account of fiscal mother company;

* Account property propagation:
    * Following fields property are propagated in all the fiscal child company:
        * product_category / property_account_income_categ;
        * product_category / property_account_expense_categ;

* Update the wizard of company creation:
    * for associated company:
        * Possibility to set the VAT number of the company;
        * possiblity to select a chart account;
        * delete some properties created by default, and give the possiblity to
          create the good ones: property_receivable, property_payable;

TODO:
-----
    * Update the description of this module;
    * Check the ir.model.access model
    * Check if account_move_line code is usefull :possibility to
      reconcile entries between differents fiscal companies (?!?)

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2013-Today, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
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
    ],
    'demo': [
        'demo/res_groups.xml',
#        'demo/account_fiscalyear.xml',
#        'demo/account_period.xml',
        'demo/account_account.xml',
        'demo/account_journal.xml',
        'demo/ir_property.xml',
    ],
    'installable': False,
    'auto_install': True,
}
