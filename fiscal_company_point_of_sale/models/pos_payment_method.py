# Copyright (C) 2025-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PosPaymentMethod(models.Model):
    _name = "pos.payment.method"
    _inherit = [
        "pos.payment.method",
        "fiscal.company.check.company.mixin",
    ]

    _fiscal_company_forbid_fiscal_type = ["group", "fiscal_mother"]
