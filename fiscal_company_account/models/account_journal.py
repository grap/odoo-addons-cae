# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountJournal(models.Model):
    _name = "account.journal"
    _inherit = [
        "account.journal",
        "fiscal.company.change.search.domain.mixin",
    ]

    def _get_journal_dashboard_data_batched(self):
        # Modify Context to add domain based on allowed companies
        # when making request on account.move
        return super(
            AccountJournal, self.with_context(add_company_domain=True)
        )._get_journal_dashboard_data_batched()

    def _get_journal_dashboard_outstanding_payments(self):
        """Oustanding payments are computed in an non overloable way.
        so in a integrated company context, it compute the values
        for the all CAE.
        Feature is so disabled in that context
        """
        if self.env.company.fiscal_type == "fiscal_child":
            return {x.id: (0, 0) for x in self}
        return super()._get_journal_dashboard_outstanding_payments()

    def _get_sale_purchase_graph_data(self):
        """Invoice amount repartition over the time is computed
        in a non overloable way, so in a integrated company context,
        it compute the values for the all CAE.
        Feature is so disabled in that context.
        """
        res = super()._get_sale_purchase_graph_data()
        if self.env.company.fiscal_type == "fiscal_child":
            for k, _v in res.items():
                res[k][0]["values"] = []
        return res

    def _get_bank_cash_graph_data(self):
        """Statement amount repartition over the time is computed
        in a non overloable way, so in a integrated company context,
        it compute the values for the all CAE.
        Feature is so disabled in that context.
        """
        res = super()._get_bank_cash_graph_data()
        if self.env.company.fiscal_type == "fiscal_child":
            for k, _v in res.items():
                res[k][0]["values"] = []
        return res
