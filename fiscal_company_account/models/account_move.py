# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = [
        "account.move",
        "fiscal.company.check.company.mixin",
    ]

    _fiscal_company_forbid_fiscal_type = ["fiscal_mother"]

    journal_id = fields.Many2one(check_company=False)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        return super(
            AccountMove, self.with_context(fiscal_company_disable_switch_company=True)
        )._onchange_partner_id()

    @api.depends("journal_id")
    def _compute_company_id(self):
        """In odoo Core, the company of an account move is the company of the journal,
        that allows to write account moves in group level.
        However, this behaviour is not correct in a CAE context.
        So we disable the call of super in this case, and set the current company.
        """
        for move in self.filtered(
            lambda x: x.journal_id.company_id.fiscal_type == "fiscal_mother"
        ):
            move.company_id = self.env.company
        return super(
            AccountMove,
            self.filtered(
                lambda x: x.journal_id.company_id.fiscal_type != "fiscal_mother"
            ),
        )._compute_company_id()

    @api.model
    def _where_calc(self, domain, active_test=True):
        """Used only in a dashboard context (see account_journal.py)
        to add extra filters, based on current allowed companies
        to filter in an integrated company context, data of other integrated
        companies of the same CAE."""
        if self.env.context.get("add_company_domain", False):
            if self.env.context.get("allowed_company_ids"):
                domain += [
                    ("company_id", "in", self.env.context.get("allowed_company_ids"))
                ]
            else:
                domain += [("company_id", "=", self.env.company.id)]
        return super()._where_calc(domain, active_test=active_test)
