This module introduce a contextual key to change the behaviour of with_company.

For exemple, in odoo/addons/account/models/account_move.py file, the following
code is present

.. code-block:: python

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self = self.with_company(self.journal_id.company_id)
        ...

That's annoying, because the company of the journal is not the same as
the company of the account move. So, in a CAE context, the company of the move
will be the integrated company, and the company of the journal will be the CAE.

So, it's possible to write the following code, to disable locally the with_company call
with the following syntax.


.. code-block:: python

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        return super(
            AccountMove, self.with_context(fiscal_company_disable_switch_company=True)
        )._onchange_partner_id()

This module also introduces 2 mixin:

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
