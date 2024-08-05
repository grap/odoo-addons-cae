# Copyright (C) 2024-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _include_fiscal_company_ids(self, company_ids):
        companies = self.env["res.company"].browse(company_ids)
        return (
            company_ids
            + companies.filtered(lambda x: x.fiscal_type == "fiscal_child")
            .mapped("parent_id")
            .ids
        )
