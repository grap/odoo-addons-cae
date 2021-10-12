# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountTax(models.Model):
    _name = "account.tax"
    _inherit = [
        "account.tax",
        "include.fiscal.company.search.mixin",
        "fiscal.child.check.mixin",
    ]

    @api.multi
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
            company = self.env.user.company_id.fiscal_company_id
            return super().filtered(lambda x: x.company_id == company)
        return super().filtered(func)
