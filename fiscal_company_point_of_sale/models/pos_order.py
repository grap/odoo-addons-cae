# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _prepare_bank_statement_line_payment_values(self, data):
        company_id = self.config_id.company_id.id
        return super(PosOrder, self.with_context(
            overload_force_company=company_id)
        )._prepare_bank_statement_line_payment_values(data)
