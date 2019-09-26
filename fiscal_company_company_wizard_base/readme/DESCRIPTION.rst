This module extend Odoo functionnalities, regarding companies features to
manage CAE (Coopearatives of Activities and Employment) that is a special
status for french companies.

This module is a glue module for the Odoo Company Wizard - Base module.

**Features**

* adds a ``fiscal_type`` field on the Company Creation wizard and constrains
  regarding this value.
* If the created company is a child company, some of the value of the mother
  company will be copied into the new child company.
