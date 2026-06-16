# Copyright (C) 2024-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "fiscal.company.check.company.mixin"]

    _fiscal_company_forbid_fiscal_type = ["group", "fiscal_mother"]
