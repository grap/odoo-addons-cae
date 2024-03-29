=============
CAE - Account
=============

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:9a71613e835148f3da9011b8a176fc70bf9cb2a379cf653c36b31e7055c0df86
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-grap%2Fodoo--addons--cae-lightgray.png?logo=github
    :target: https://github.com/grap/odoo-addons-cae/tree/12.0/fiscal_company_account
    :alt: grap/odoo-addons-cae

|badge1| |badge2| |badge3|

This module extend Odoo functionnalities, regarding companies features to
manage CAE (Coopearatives of Activities and Employment) that is a special
status for french companies.

**Features**

* Add constrains on ``account.bank.statement``, ``account.invoice``
  ``account.move``, ``account.move.line``, ``account.payment`` models
  that prevent to create such items on a fiscal mother company.

* Account property propagation:
    * Following fields property are propagated in all the fiscal child company:
        * product_category / property_account_income_categ_id;
        * product_category / property_account_expense_categ_id;

**Table of contents**

.. contents::
   :local:

Development
===========

* For the migration to V>12, take care of the tax.filtered occurences in
  Odoo and OCA modules.
  There are a lot of ``filtered(lambda x: x.company_id == current_company)``
  in Odoo. The module ``fiscal_company_account`` alter the behaviour of the function
  ``filtered`` of the ``account.tax`` module, to filter on the mother fiscal company.
  However, the changes is imperfect, and multiple filters (company and not company filters)
  will fail.
  During migration, please run:
  ``rgrep "tax.*filtered.*company_id"``

Known issues / Roadmap
======================

* the odoo accounting dashboard is disabled, because all the data are bad
  computed. (by SQL request), so security access is not possible.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/grap/odoo-addons-cae/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/grap/odoo-addons-cae/issues/new?body=module:%20fiscal_company_account%0Aversion:%2012.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* GRAP

Contributors
~~~~~~~~~~~~

* Julien WESTE
* Sylvain LE GAL <https://twitter.com/legalsylvain>

Other credits
~~~~~~~~~~~~~

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)

Porting from odoo V8 to odoo V10 has been funded by :
   * BABEL.COOP, leverage cooperation through the digital age (<http://babel.coop>)

Maintainers
~~~~~~~~~~~

This module is part of the `grap/odoo-addons-cae <https://github.com/grap/odoo-addons-cae/tree/12.0/fiscal_company_account>`_ project on GitHub.

You are welcome to contribute.
