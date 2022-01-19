This module is a glue module between ``recurring_consignement`` module
and ``fiscal_company_base`` module.

* When creating a new consignor, the recurring_consignment module
  create a new ``account.account``. by default, the company_id is the current
  company of the user. This module select the fiscal company of the current user.
