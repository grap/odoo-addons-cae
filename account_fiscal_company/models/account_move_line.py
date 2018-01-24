# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from openerp import tools
from openerp import netsvc
from openerp.osv.orm import Model
from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_move_line(Model):
    _name = 'account.move.line'
    _inherit = 'account.move.line'

    _columns = {
        'company_id': fields.many2one('res.company',
                                      string='Company',
                                      required=True)
    }

    def _check_company_id(self, cr, uid, ids, context=None):
        lines = self.browse(cr, uid, ids, context=context)
        for l in lines:
            if (l.company_id.fiscal_company != l.account_id.company_id or
                    l.company_id.fiscal_company != l.period_id.company_id):
                return False
        return True

    _constraints = [
        (_check_company_id, 'Company must be the same for its related \
        account and period.', ['company_id']),
    ]

    def _query_get(self, cr, uid, obj='l', context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        company_list = [c.id for c in user.company_id.fiscal_childs]
        company = user.company_id.id
        if company not in company_list:
            company_list.append(company)
        company_list = str(tuple(company_list))
        if company_list[-2:-1] == ',':
            company_list = company_list[:-2] + ')'
        return super(account_move_line, self)\
            ._query_get(cr, uid, obj=obj, context=context) + \
            " AND " + obj + ".company_id IN " + company_list

    def reconcile(self, cr, uid, ids, type='auto',
                  writeoff_acc_id=False, writeoff_period_id=False,
                  writeoff_journal_id=False, context=None):
        account_obj = self.pool.get('account.account')
        move_obj = self.pool.get('account.move')
        move_rec_obj = self.pool.get('account.move.reconcile')
        partner_obj = self.pool.get('res.partner')
        currency_obj = self.pool.get('res.currency')
        lines = self.browse(cr, uid, ids, context=context)
        unrec_lines = filter(lambda x: not x['reconcile_id'], lines)
        credit = debit = 0.0
        currency = 0.0
        account_id = False
        partner_id = False
        if context is None:
            context = {}
        company_list = []
        for line in self.browse(cr, uid, ids, context=context):
            if (company_list and
                    line.company_id.fiscal_company.id not in company_list):
                raise osv.except_osv(_('Warning !'), _(
                    """To reconcile the entries company should be the same"""
                    """ for all entries"""))
            company_list.append(line.company_id.fiscal_company.id)
        for line in unrec_lines:
            if line.state != 'valid':
                raise osv.except_osv(
                    _('Error'),
                    _('Entry "%s" is not valid !') % line.name)
            credit += line['credit']
            debit += line['debit']
            currency += line['amount_currency'] or 0.0
            account_id = line['account_id']['id']
            partner_id = (line['partner_id'] and line['partner_id']['id'])\
                or False
        writeoff = debit - credit

        # Ifdate_p in context => take this date
        date = context.get('date_p')\
            or time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT)

        cr.execute("""
            SELECT account_id, reconcile_id
            FROM account_move_line
            WHERE id IN %s
            GROUP BY account_id,reconcile_id""",
                   (tuple(ids), ))
        r = cr.fetchall()
        # TODO: move this check to a constraint in
        # the account_move_reconcile object
        if not unrec_lines:
            raise osv.except_osv(_('Error'), _('Entry is already reconciled'))
        account = account_obj.browse(cr, uid, account_id, context=context)
        if r[0][1] is not None:
            raise osv.except_osv(
                _('Error'),
                _('Some entries are already reconciled !'))

        if context.get('fy_closing'):
            # We don't want to generate any write-off when being called from
            # the wizard used to close a fiscal year (and it doesn't give us
            # any writeoff_acc_id).
            pass
        elif ((not currency_obj.is_zero(
                cr, uid, account.company_id.currency_id, writeoff)) or
                (account.currency_id and
                    (not currency_obj.is_zero(
                        cr, uid, account.currency_id, currency)))):
            if not writeoff_acc_id:
                raise osv.except_osv(
                    _('Warning'), _(
                        """You have to provide an account for"""
                        """ the write off/exchange difference entry !"""))
            if writeoff > 0:
                debit = writeoff
                credit = 0.0
                self_credit = writeoff
                self_debit = 0.0
            else:
                debit = 0.0
                credit = -writeoff
                self_credit = 0.0
                self_debit = -writeoff
            # If comment exist in context, take it
            if 'comment' in context and context['comment']:
                libelle = context['comment']
            else:
                libelle = _('Write-Off')

            cur_obj = self.pool.get('res.currency')
            cur_id = False
            amount_currency_writeoff = 0.0
            if (context.get('company_currency_id', False) !=
                    context.get('currency_id', False)):
                cur_id = context.get('currency_id', False)
                for line in unrec_lines:
                    if (line.currency_id and
                            line.currency_id.id ==
                            context.get('currency_id', False)):
                        amount_currency_writeoff += line.amount_currency
                    else:
                        tmp_amount = cur_obj.compute(
                            cr, uid, line.account_id.company_id.currency_id.id,
                            context.get('currency_id', False),
                            abs(line.debit - line.credit),
                            context={'date': line.date})
                        amount_currency_writeoff += (
                            (line.debit > 0) and
                            tmp_amount or -tmp_amount)

            writeoff_lines = [
                (0, 0, {
                    'name': libelle,
                    'debit': self_debit,
                    'credit': self_credit,
                    'account_id': account_id,
                    'date': date,
                    'partner_id': partner_id,
                    'currency_id': cur_id or (account.currency_id.id or False),
                    'amount_currency': (
                        amount_currency_writeoff and
                        (-1 * amount_currency_writeoff) or
                        (account.currency_id.id and -1 * currency or 0.0))
                }),
                (0, 0, {
                    'name': libelle,
                    'debit': debit,
                    'credit': credit,
                    'account_id': writeoff_acc_id,
                    'analytic_account_id': context.get('analytic_id', False),
                    'date': date,
                    'partner_id': partner_id,
                    'currency_id': cur_id or (account.currency_id.id or False),
                    'amount_currency': (
                        amount_currency_writeoff and
                        amount_currency_writeoff or
                        (account.currency_id.id and currency or 0.0))
                })
            ]

            writeoff_move_id = move_obj.create(cr, uid, {
                'period_id': writeoff_period_id,
                'journal_id': writeoff_journal_id,
                'date': date,
                'state': 'draft',
                'line_id': writeoff_lines
            })

            writeoff_line_ids = self.search(
                cr, uid, [
                    ('move_id', '=', writeoff_move_id),
                    ('account_id', '=', account_id)])
            if account_id == writeoff_acc_id:
                writeoff_line_ids = [writeoff_line_ids[1]]
            ids += writeoff_line_ids
        try:
            r_id = move_rec_obj.create(cr, uid, {
                'type': type,
                'line_id': map(lambda x: (4, x, False), ids),
                'line_partial_ids': map(lambda x: (3, x, False), ids)
            })
            wf_service = netsvc.LocalService("workflow")
            # the id of the move.reconcile is written in the move.line (self)
            # by the create method above because of the way the line_id
            # are defined: (4, x, False)
            for id in ids:
                wf_service.trg_trigger(uid, 'account.move.line', id, cr)

            if lines and lines[0]:
                partner_id = (
                    lines[0].partner_id and lines[0].partner_id.id or False)
                if (
                    partner_id and context and
                        context.get('stop_reconcile', False)):
                    partner_obj.write(
                        cr, uid, [partner_id], {
                            'last_reconciliation_date': (
                                time.strftime('%Y-%m-%d %H:%M:%S'))})
            return r_id
        except:
            return False

    def reconcile_partial(
            self, cr, uid, ids, type='auto', context=None,
            writeoff_acc_id=False, writeoff_period_id=False,
            writeoff_journal_id=False):
        move_rec_obj = self.pool.get('account.move.reconcile')
        merges = []
        unmerge = []
        total = 0.0
        merges_rec = []
        company_list = []
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            if (company_list and
                    line.company_id.fiscal_company.id not in company_list):
                raise osv.except_osv(
                    _('Warning!'), _(
                        """To reconcile the entries company should be the"""
                        """ same for all entries."""))
            company_list.append(line.company_id.fiscal_company.id)

        for line in self.browse(cr, uid, ids, context=context):
            if line.account_id.currency_id:
                currency_id = line.account_id.currency_id
            else:
                currency_id = line.company_id.currency_id
            if line.reconcile_id:
                raise osv.except_osv(_('Warning'), _(
                    """Journal Item '%s' (id: %s), Move '%s' is already"""
                    """ reconciled!""") % (
                    line.name, line.id, line.move_id.name))
            if line.reconcile_partial_id:
                for line2 in line.reconcile_partial_id.line_partial_ids:
                    if not line2.reconcile_id:
                        if line2.id not in merges:
                            merges.append(line2.id)
                        if line2.account_id.currency_id:
                            total += line2.amount_currency
                        else:
                            total += (
                                (line2.debit or 0.0) -
                                (line2.credit or 0.0))
                merges_rec.append(line.reconcile_partial_id.id)
            else:
                unmerge.append(line.id)
                if line.account_id.currency_id:
                    total += line.amount_currency
                else:
                    total += (line.debit or 0.0) - (line.credit or 0.0)
        if self.pool.get('res.currency').is_zero(cr, uid, currency_id, total):
            res = self.reconcile(
                cr, uid, merges + unmerge, context=context,
                writeoff_acc_id=writeoff_acc_id,
                writeoff_period_id=writeoff_period_id,
                writeoff_journal_id=writeoff_journal_id)
            return res
        r_id = move_rec_obj.create(cr, uid, {
            'type': type,
            'line_partial_ids': map(lambda x: (4, x, False), merges + unmerge)
        }, context=context)
        move_rec_obj.reconcile_partial_check(
            cr, uid, [r_id] + merges_rec, context=context)
        return True
