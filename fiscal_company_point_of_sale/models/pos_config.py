# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = "pos.config"

    # Overwrite company constrains
    @api.constrains("company_id", "invoice_journal_id")
    def _check_company_invoice_journal(self):
        if (
            self.invoice_journal_id
            and self.invoice_journal_id.company_id.fiscal_company_id.id
            != self.company_id.fiscal_company_id.id
        ):
            raise ValidationError(
                _(
                    "The company of the invoice journal and the company of the point of sale"
                    " must have the same fiscal company."
                )
            )

    @api.constrains("company_id", "journal_id")
    def _check_company_journal(self):
        if (
            self.journal_id
            and self.journal_id.company_id.fiscal_company_id.id
            != self.company_id.fiscal_company_id.id
        ):
            raise ValidationError(
                _(
                    "The company of the sales journal and the company of the point of sale"
                    " must have the same fiscal company."
                )
            )

    @api.constrains("company_id", "journal_ids")
    def _check_company_payment(self):
        if self.mapped("journal_ids.company_id.fiscal_company_id.id") != [
            self.company_id.fiscal_company_id.id
        ]:
            raise ValidationError(
                _(
                    "The companies of the method payments and the company of the point of sale"
                    " must have the same fiscal company."
                )
            )
