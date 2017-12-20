.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================
Manage Cooperatives of Activities and Employment
================================================

This module extend Odoo functionnalities, regarding companies features to
manage CAE (Coopearatives of Activities and Employment) that is a special
status for french companies.

(see above, links that describe what is CAE).

Basically, in a CAE, there is a 'parent' company that hosts many 'child'
companies. People in a child company should have access only to their activity.
(account moves, customers, suppliers, products, etc...)

In a fiscal and legal point of view, there is only one company (the parent one)
so there is only on chart of accounts. So accounting moves of the child
companies are written in the child company, but associated to the account of
the parent company.

Companies feature
-----------------

* Add a trigram field on res_company
* Add field 'fiscal_company' that and 'fiscal_type' in the table res_company;
* A company can be 'normal', 'fiscal_mother' or 'fiscal_child';

Add a wizard to create more easily child companies.

.. image:: /base_fiscal_company/static/description/company_wizard.png

Users Feature
-------------

* If a user has access rights to a 'fiscal_mother' so he has access
  rights to all 'fiscal_child' companies;

More information about CAE [FR]
-------------------------------

* https://fr.wikipedia.org/wiki/Coopérative_d'activités_et_d'emploi
* http://www.cooperer.coop/
* http://www.copea.fr/


Limits / Roadmaps / TODO
------------------------

- rename odoo-addons-cis -> odoo-addons-cae;
- rename xxx_fiscal_company -> cae
- rename 'fiscal_type' into cae_type : normal / cae_child / cae_parent
- rename 'fiscal_company' into 'fiscal_company_id'

* Created partner from users / companies, must be disabled by default.
  (maybe create a new module for that feature)
* Add a m2m fields on company to have the list of users.

Installation
============

Normal installation.

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL <https://twitter.com/legalsylvain>
