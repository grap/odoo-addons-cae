# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "fiscal.mother.check.mixin"]

    company_id = fields.Many2one(
        related=False, default=lambda x: x._default_company_id()
    )

    def _default_company_id(self):
        if self.env.context.get("force_company", False):
            return self.env.context["force_company"]
        if self.env.context.get("company_id", False):
            return self.env.context["company_id"]
        return self.env.user.company_id.id
