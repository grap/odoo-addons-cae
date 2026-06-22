# Copyright (C) 2018-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "fiscal.company.check.company.mixin"]

    _fiscal_company_forbid_fiscal_type = ["group", "fiscal_mother"]

    payment_term_id = fields.Many2one(check_company=False)

    # For pos_order_to_sale_order module to avoid AccessError
    # during _recompute_taxes launch with sale order creation
    #
    # In fact, _compute_tax_id (sale.order.line) use fiscal_company.
    # Without this code, allowed_company_ids is recalculated in
    # odoo/api.py def company(self) function with fiscal_company +
    # user_company_ids → these can't be different.
    def _recompute_taxes(self):
        ctx = dict(self.env.context)

        if ctx.get("pos_order_lines_data"):
            ctx["fiscal_company_disable_switch_company"] = True

        return super(SaleOrder, self.with_context(**ctx))._recompute_taxes()
