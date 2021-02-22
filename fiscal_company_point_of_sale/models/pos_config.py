# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    @api.constrains("company_id", "invoice_journal_id")
    def _check_company_invoice_journal(self):
        return True

    @api.constrains("company_id", "journal_id")
    def _check_company_journal(self):
        return True
