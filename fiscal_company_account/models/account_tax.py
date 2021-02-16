# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountTax(models.Model):
    _name = "account.tax"
    _inherit = ["account.tax", "include.fiscal.company.search.mixin"]

    # TODO, document this function
    @api.multi
    def filtered(self, func):
        if callable(func) and func.__code__.co_names == ("company_id",):
            company = self.env.user.company_id.fiscal_company_id
            return super().filtered(lambda x: x.company_id == company)
        return super().filtered(func)
