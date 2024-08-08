# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models

with_company_original = models.BaseModel.with_company


def with_company(self, company):
    if self.env.context.get("fiscal_company_disable_switch_company", False):
        return self
    return with_company_original(self, company)


models.BaseModel.with_company = with_company
