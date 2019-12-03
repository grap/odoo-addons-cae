This module extend Odoo functionnalities, regarding companies features to
manage CAE (Coopearatives of Activities and Employment) that is a special
status for french companies.

This module is a glue module for the Odoo Product module.

**Features**

* User in mother company can see product of all child company
* User in fiscal company can see but not update / delete product
  of mother company
* Add a field ```cae_administrative_ok``` on ```product.product```. if checked
  the product will not be updatable by non 'CAE Manager' users
