# Copyright (C) 2018-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "fiscal.company.check.company.mixin"]

    _fiscal_company_forbid_fiscal_type = ["group", "fiscal_mother"]

    payment_term_id = fields.Many2one(check_company=False)
