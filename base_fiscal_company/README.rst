.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================
Manage Cooperatives of Activities and Employment
================================================

This module extend Odoo functionnalities, regarding companies features to
manage CAE (Coopearatives of Activities and Employment) that is a special
status for french companies.

(see above, links that describes what is CAE).

Basically, in a CAE, there is a 'parent' company that hosts many 'child'
companies. People in a child company should have access only to their activity.
(account moves, customers, suppliers, products, etc...)

In a fiscal and legal point of view, there is only one company (the parent one)
so there is only on chart of accounts. Accounting moves of the child
companies are written in the child company, but associated to the account of
the parent company.

Companies feature
-----------------

* Add a new field on company `fiscal_type`:
    * `normal` : classical company
    * `fiscal_mother`: CAE company, that can host many child companies
    * `fiscal_child`: child company, hosted by the CAE

* Add a new field on company `fiscal_code` that is required for fiscal
  child companies, and that is used to identify simply a company.

Add a wizard to create more easily child companies.

.. image:: /base_fiscal_company/static/description/company_wizard.png

Users Feature
-------------

* If a user has access rights to a 'fiscal_mother' so he has access
  rights to all 'fiscal_child' companies;

Groups Feature
--------------

* this module add a new group 'Disabled Features for Fiscal Company'
  that should be affected to all the features bad designed by odoo,
  specially when odoo introduced views based on datas computed on SQL hard
  coded requests that can not work with the Odoo CAE design.
  See 'account_fiscal_company' module for exemples.

More information about CAE [FR]
-------------------------------

* https://fr.wikipedia.org/wiki/Coopérative_d'activités_et_d'emploi
* http://www.cooperer.coop/
* http://www.copea.fr/

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL <https://twitter.com/legalsylvain>
