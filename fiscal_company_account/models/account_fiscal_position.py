# Copyright (C) 2026-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountFiscalPosition(models.Model):
    _name = "account.fiscal.position"
    _inherit = [
        "account.fiscal.position",
        "fiscal.company.change.search.domain.mixin",
    ]
