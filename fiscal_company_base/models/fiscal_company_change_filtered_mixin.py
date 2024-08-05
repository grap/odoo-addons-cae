# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class FiscalCompanyChangeFilteredMixin(models.AbstractModel):
    """This abstract change the filtered features for models.

    if a filtered is call with "lambda x: x.company_id = company_id"
    it will be replace by ('company_id', '=', fiscal_company_id)
    """

    _name = "fiscal.company.change.filtered.mixin"
    _description = "Fiscal Company : Change Filtered Mixin"

    def filtered(self, func):
        # a lot of function in Odoo are filtering taxes by the current company
        # for exemple in 'addons/account/models/account_invoice.py#L1809'
        # In our CAE case, we replace the current company by the fiscal one.

        # TODO, improve that ugly code.
        if (
            not self.env.context.get("dont_change_filter", False)
            and callable(func)
            and "company_id" in func.__code__.co_names
        ):
            company = self.env.company.fiscal_company_id
            return super().filtered(lambda x: x.company_id == company)
        return super().filtered(func)
