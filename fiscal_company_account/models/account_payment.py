# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    destination_account_id = fields.Many2one(check_company=False)

    outstanding_account_id = fields.Many2one(check_company=False)
