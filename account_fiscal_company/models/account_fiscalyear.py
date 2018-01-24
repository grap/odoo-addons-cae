# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from ..decorator import new_api_switch_company_period


class AccountFiscalyear(models.Model):
    _inherit = 'account.fiscalyear'

    @api.model
    @new_api_switch_company_period
    def find(self, dt=None, exception=True):
        return super(AccountFiscalyear, self).find(dt=dt, exception=exception)
