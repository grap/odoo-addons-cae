# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.depends("country_id", "parent_id.country_id", "fiscal_type")
    def compute_account_tax_fiscal_country(self):
        for company in self.filtered(lambda x: x.fiscal_type == "fiscal_child"):
            company.account_fiscal_country_id = company.parent_id.country_id

        return super(
            ResCompany, self.filtered(lambda x: x.fiscal_type != "fiscal_child")
        ).compute_account_tax_fiscal_country()
