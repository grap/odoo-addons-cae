# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = [
        "res.partner",
        "fiscal.company.check.company.mixin",
        "fiscal.company.change.search.domain.mixin",
        "fiscal.company.propagate.child.company.mixin",
    ]

    _fiscal_company_forbid_fiscal_type = ["group", "fiscal_mother"]

    def _fiscal_company_forbid_fiscal_type_allow_exceptions(self):
        res = super()._fiscal_company_forbid_fiscal_type_allow_exceptions()
        partner_users = (
            self.env["res.users"]
            .with_context(active_test=False)
            .search([])
            .mapped("partner_id")
        )
        res = res.filtered(lambda x: x not in partner_users)
        return res
