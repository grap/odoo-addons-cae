.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================
Manage Cooperatives of Activities and Employment - Account
==========================================================

This module extend Odoo functionnalities, regarding companies features to
manage CAE (Coopearatives of Activities and Employment) that is a special
status for french companies.

Features
========

* Add constrains on ``account.bank.statement``, ``account.invoice``
  ``account.move``, ``account.move.line``, ``account.payment`` models
  that prevent to create such items on a fiscal mother company.

* Account property propagation:
    * Following fields property are propagated in all the fiscal child company:
        * product_category / property_account_income_categ;
        * product_category / property_account_expense_categ;

Know issues / Roadmap
=====================

* the odoo accounting dashboard is disabled, because all the data are bad
  computed. (by SQL request), so security access is not possible.

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL <https://twitter.com/legalsylvain>

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (<http://www.grap.coop>)
