# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _prepare_bank_statement_line_payment_values(self, data):
        company_id = self.config_id.company_id.id
        return super(PosOrder, self.with_context(
            overload_force_company=company_id)
        )._prepare_bank_statement_line_payment_values(data)

    # The call of this function is made with a force company that
    # point on the sale journal company, that is wrong in CAE
    # where there is a single shared journal for many companies
    # we so reforce the value force_company with the correct
    # company_id for the two following function
    def _create_account_move(self, dt, ref, journal_id, company_id):
        if not len(self):
            return super()._create_account_move(dt, ref, journal_id, company_id)
        company_id = self[0].config_id.company_id.id
        return super(
            PosOrder, self.with_context(force_company=company_id)
        )._create_account_move(dt, ref, journal_id, company_id)

    @api.multi
    def _create_account_move_line(self, session=None, move=None):
        company_id = self[0].config_id.company_id.id
        return super(
            PosOrder, self.with_context(force_company=company_id)
        )._create_account_move_line(session=session, move=move)
