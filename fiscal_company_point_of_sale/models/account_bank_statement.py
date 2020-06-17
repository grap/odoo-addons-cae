# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.model
    def create(self, vals):
        if "company_id" not in vals and "company_id" in self.env.context:
            vals["company_id"] = self.env.context["company_id"]
        return super().create(vals)
