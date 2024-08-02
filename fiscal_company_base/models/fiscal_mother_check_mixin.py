# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, models
from odoo.exceptions import ValidationError


class FiscalMotherCheckMixin(models.AbstractModel):
    """This abstract block the possibility for a model to have
    items linked to a fiscal mother company.
    Note that you can only inherit from this abstract, if the current model
    has ```company_id``` and ```name``` fields defined.
    """

    _name = "fiscal.mother.check.mixin"
    _description = "Fiscal Mother Check Mixin"

    @api.constrains("company_id")
    def _check_fiscal_child_company_id(self):
        bad_items = self.filtered(lambda x: x.company_id.fiscal_type == "fiscal_mother")
        if bad_items:
            raise ValidationError(
                _(
                    "You can't affect the item(s) %s to a Fiscal"
                    " Mother company.\n\n"
                    " (model '%s')"
                )
                % (",".join([x.name for x in bad_items]), self._name)
            )
