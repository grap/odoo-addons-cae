# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv.orm import Model
from openerp.addons.account_fiscal_company.decorator import \
    switch_company, \
    add_user_company


class account_account(Model):
    _inherit = 'account.account'

    @switch_company
    def search(
            self, cr, uid, args, offset=0, limit=None,
            order=None, context=None, count=False):
        return super(account_account, self).search(
            cr, uid, args, offset=offset, limit=limit, order=order,
            context=context, count=count)

    @add_user_company
    def compute(
            self, cr, uid, ids, field_names, arg=None, context=None, query='',
            query_params=()):
        return super(account_account, self).__compute(
            cr, uid, ids=ids, field_names=field_names, arg=arg,
            context=context, query=query, query_params=query_params)
