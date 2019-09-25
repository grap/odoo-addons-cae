# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from ..decorator import switch_company


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @switch_company
    def search(
            self, args, offset=0, limit=None, order=None, count=False):
        return super().search(
            args, offset=offset, limit=limit, order=order, count=count)

    @api.multi
    def filtered(self, func):
        if callable(func) and func.__code__.co_names == ('company_id',):
            company = self.env.user.company_id.fiscal_company_id
            return super().filtered(
                lambda x: x.company_id == company)
        return super().filtered(func)
