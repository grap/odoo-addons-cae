# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountJournal(models.Model):
    _name = 'account.journal'
    _inherit = ['account.journal', 'include.fiscal.company.search.mixin']
