# Copyright (C) 2024-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountFiscalYear(models.Model):
    _name = "account.fiscal.year"
    _inherit = [
        "account.fiscal.year",
        "fiscal.company.change.search.domain.mixin",
        "fiscal.company.change.filtered.mixin",
        "fiscal.company.check.company.mixin",
    ]

    _fiscal_company_forbid_fiscal_type = ["fiscal_child", "group"]
