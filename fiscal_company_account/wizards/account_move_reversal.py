# Copyright (C) 2025-Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    journal_id = fields.Many2one(check_company=False)
