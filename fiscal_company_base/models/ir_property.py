# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class IrProperty(models.Model):
    _inherit = "ir.property"

    @api.model
    def get(self, name, model, res_id=False):
        if (
            "overload_force_company" in self.env.context
            and "force_company" in self.env.context
        ):
            return super(
                IrProperty,
                self.with_context(
                    force_company=self.env.context.get("overload_force_company")
                ),
            ).get(name, model, res_id=res_id)
        else:
            return super().get(name, model, res_id=res_id)
