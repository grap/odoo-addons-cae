# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def load_for_current_company(self, sale_tax_rate, purchase_tax_rate):
        res = super().load_for_current_company(sale_tax_rate, purchase_tax_rate)

        # Create properties for all the categories
        # for all the new created accounts
        ProductCategory = self.env["product.category"]
        categories = ProductCategory.with_context(active_test=False).search([])
        for category in categories:
            for field_name in [
                "global_property_account_expense_categ",
                "global_property_account_income_categ",
            ]:
                category._apply_global_account_property(
                    self.env.user.company_id, field_name
                )
        return res
