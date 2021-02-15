# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountReconciliationWidget(models.AbstractModel):
    _inherit = 'account.reconciliation.widget'

    @api.model
    def _set_domain_to_current_company(self, domain):
        result = []
        for item in domain:
            if 'company_id' in str(item):
                result.append(
                    ('company_id', '=', self.env.user.company_id.id)
                )
            else:
                result.append(item)
        return result

    @api.model
    def _domain_move_lines_for_reconciliation(
            self, st_line, aml_accounts, partner_id, excluded_ids=None,
            search_str=False):
        domain = super()._domain_move_lines_for_reconciliation(
            st_line, aml_accounts, partner_id, excluded_ids=excluded_ids,
            search_str=search_str)
        return self._set_domain_to_current_company(domain)

    @api.model
    def _domain_move_lines_for_manual_reconciliation(
            self, account_id, partner_id=False, excluded_ids=None,
            search_str=False):
        domain = super()._domain_move_lines_for_manual_reconciliation(
            account_id, partner_id=False, excluded_ids=None,
            search_str=search_str)
        return self._set_domain_to_current_company(domain)
