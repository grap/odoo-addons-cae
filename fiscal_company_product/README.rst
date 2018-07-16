.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================
Manage Cooperatives of Activities and Employment - Product
==========================================================


This module extend Odoo functionnalities, regarding companies features to
manage CAE (Coopearatives of Activities and Employment) that is a special
status for french companies.

Features
--------

* user in mother company can see product of all child company
* user in fiscal company can see but not update / delete product
  of mother company
* Add a field ```cae_administrative_ok``` on ```product.product```. if checked
  the product will not be updatable by non 'CAE Manager' users

Company Creation Wizard
-----------------------

* Create a Sale Pricelist and the according property to
  ```property_product_pricelist```

Installation
============

Normal installation.

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL <https://twitter.com/legalsylvain>
