# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model
from openerp.osv import fields


class account_bank_statement(Model):
    _name = 'account.bank.statement'
    _inherit = 'account.bank.statement'

    _columns = {
        'company_id': fields.many2one('res.company',
                                      string='Company',
                                      required=True)
    }

    def _check_company_id(self, cr, uid, ids, context=None):
        for statement in self.browse(cr, uid, ids, context=context):
            if (statement.company_id.fiscal_company !=
                    statement.period_id.company_id.fiscal_company):
                return False
        return True

    _constraints = [
        (_check_company_id, 'The journal and period chosen have \
        to belong to the same company.', ['journal_id', 'period_id']),
    ]
