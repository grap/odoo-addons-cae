# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountTax(models.Model):
    _name = "account.tax"
    _inherit = [
        "account.tax",
        "fiscal.company.change.search.domain.mixin",
        "fiscal.company.change.filtered.mixin",
        "fiscal.company.check.company.mixin",
    ]

    _fiscal_company_forbid_fiscal_type = ["fiscal_child"]
