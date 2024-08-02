# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, models
from odoo.exceptions import ValidationError


class FiscalCompanyCheckCompanyMixin(models.AbstractModel):
    """This abstract block the possibility for a model to have
    items linked to a company for some fiscal types.
    Note that you can only inherit from this abstract, if the current model
    has `company_id` fields defined.
    """

    _name = "fiscal.company.check.company.mixin"
    _description = "Fiscal Company : Check Company Mixin"

    _fiscal_company_forbid_fiscal_type = []

    @api.constrains("company_id")
    def _fiscal_company_check_company_id(self):
        bad_items = self.with_context(dont_change_filter=True).filtered(
            lambda x: x.company_id.fiscal_type
            in self._fiscal_company_forbid_fiscal_type
        )
        if bad_items:
            raise ValidationError(
                _(
                    "You can't affect the %(items_qty)s item(s) to company"
                    " with such fiscal type.\n\n"
                    " (model '%(model_name)s')",
                    items_qty=len(bad_items),
                    model_name=self._name,
                )
            )
