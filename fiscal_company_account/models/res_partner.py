# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_coa_installed = fields.Boolean(compute="_compute_is_coa_installed")

    def _fiscal_property_creation_list(self):
        res = super()._fiscal_property_creation_list()
        res += [
            "property_account_payable_id",
            "property_account_receivable_id",
        ]
        return res

    def _compute_is_coa_installed(self):
        result = bool(self.env.company.fiscal_company_id.chart_template_id)
        for partner in self:
            partner.is_coa_installed = result
