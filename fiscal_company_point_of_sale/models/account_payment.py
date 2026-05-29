# # Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# # @author: Sylvain LE GAL
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    force_outstanding_account_id = fields.Many2one(check_company=False)
