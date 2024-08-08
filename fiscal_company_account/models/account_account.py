# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAccount(models.Model):
    _name = "account.account"
    _inherit = [
        "account.account",
        "fiscal.company.change.search.domain.mixin",
        "fiscal.company.check.company.mixin",
    ]

    _fiscal_company_forbid_fiscal_type = ["fiscal_child"]

    company_id = fields.Many2one(default=lambda self: self._default_company_id())

    def _default_company_id(self):
        return self.env.company.fiscal_company_id
