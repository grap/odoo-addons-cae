# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class FiscalCompanyPropagateChildCompanyMixin(models.AbstractModel):
    """This abstract allow to propagate properties of mother companies
    in child companies context.
    - When creating a new child company, all the properties defined
      at mother company will be set in the new child company.
    """

    _name = "fiscal.company.propagate.child.company.mixin"
    _description = "Fiscal Company : Propagate in Child Company Mixin"

    @api.model
    def _fiscal_property_creation_list(self):
        """Overload me to define property fields to create to a new
        fiscal company
        """
        return []
