.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================
Manage Cooperatives of Activities and Employment - Account
==========================================================

This module extend Odoo functionnalities, regarding companies features to
manage CAE (Coopearatives of Activities and Employment) that is a special
status for french companies.

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


Installation
============

Normal installation.

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL <https://twitter.com/legalsylvain>
