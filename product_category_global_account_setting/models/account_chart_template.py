# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _load(self, company):
        res = super()._load(company)

        # Create properties for all the categories
        # for all the new created accounts
        ProductCategory = self.env["product.category"]
        categories = ProductCategory.with_context(active_test=False).search([])
        for category in categories:
            for field_name in [
                "global_property_account_expense_categ",
                "global_property_account_income_categ",
            ]:
                category._apply_global_account_property(self.env.company, field_name)
        return res
