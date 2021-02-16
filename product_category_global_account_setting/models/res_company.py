# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def create(self, vals):
        company = super().create(vals)
        if vals.get("fiscal_type") == "fiscal_child":
            company._apply_global_account_settings()
        return company

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if vals.get("fiscal_type") == "fiscal_child":
            for company in self:
                company._apply_global_account_settings()
        return res

    @api.multi
    def _apply_global_account_settings(self):
        self.ensure_one()
        ProductCategory = self.env["product.category"]
        categories = ProductCategory.with_context(active_test=False).search([])
        for category in categories:
            category._apply_global_account_property(
                self, "global_property_account_expense_categ")
            category._apply_global_account_property(
                self, "global_property_account_income_categ")
