This module introduces 2 mixin:

``fiscal.company.change.search.domain.mixin``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

the model that inherits this abstract will change the domain
in the search feature. If a domain contains ('company_id', '=', X)
it will be changed into ('company_id', 'in', [X, A, B])
if X is a CAE and A and B are the integrated related companies.

**Usage**

.. code-block:: python

  class MyModel(models.Model):
      _name = "my.model"
      _inherit = ["fiscal.company.change.search.domain.mixin"]

``fiscal.company.check.company.mixin``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The model that inherits this abstract will prevent to
create items with companies, depending on the
fiscal_type of the company.

**Usage**

.. code-block:: python

  class MyModel(models.Model):
      _name = "my.model"
      _inherit = ["fiscal.company.check.company.mixin"]

      _fiscal_company_forbid_fiscal_type = ["fiscal_mother"]
