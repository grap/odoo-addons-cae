# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        for company, vals in zip(companies, vals_list, strict=True):
            if vals.get("fiscal_type") == "fiscal_child":
                company._apply_global_account_settings()
        return companies

    def write(self, vals):
        res = super().write(vals)
        if vals.get("fiscal_type") == "fiscal_child":
            for company in self:
                company._apply_global_account_settings()
        return res

    def _apply_global_account_settings(self):
        self.ensure_one()
        ProductCategory = self.env["product.category"]
        categories = ProductCategory.with_context(active_test=False).search([])
        for category in categories:
            category._apply_global_account_property(
                self, "global_property_account_expense_categ"
            )
            category._apply_global_account_property(
                self, "global_property_account_income_categ"
            )
