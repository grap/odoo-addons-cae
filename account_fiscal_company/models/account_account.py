# coding: utf-8
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, fields, models
from odoo.addons.account_fiscal_company.decorator import switch_company


class AccountAccount(models.Model):
    _inherit = 'account.account'

    @switch_company
    def search(
            self, args, offset=0, limit=None, order=None, count=False):
        return super(AccountAccount, self).search(
            args, offset=offset, limit=limit, order=order, count=count)

## TODO or remove
##    @add_user_company
##    def compute(
##            self, cr, uid, ids, field_names, arg=None, context=None, query='',
##            query_params=()):
##        return super(account_account, self).__compute(
##            cr, uid, ids=ids, field_names=field_names, arg=arg,
##            context=context, query=query, query_params=query_params)
