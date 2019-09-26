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
