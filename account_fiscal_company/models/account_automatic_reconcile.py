# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv import osv
from openerp.tools.translate import _


class account_automatic_reconcile(osv.osv_memory):
    _inherit = 'account.automatic.reconcile'

    def reconcile(self, cr, uid, ids, context=None):
        move_line_obj = self.pool.get('account.move.line')
        obj_model = self.pool.get('ir.model.data')
        company_id = self.pool.get('res.users').browse(
            cr, uid, uid, context).company_id.id
        journal_ids = self.pool.get('account.journal').search(cr, uid, [])
        journal_ids = tuple(journal_ids)
        if context is None:
            context = {}
        form = self.browse(cr, uid, ids, context=context)[0]
        max_amount = form.max_amount or 0.0
        power = form.power
        allow_write_off = form.allow_write_off
        reconciled = unreconciled = 0
        if not form.account_ids:
            raise osv.except_osv(
                _('UserError'),
                _('You must select accounts to reconcile'))
        for account_id in form.account_ids:
            # reconcile automatically all transactions from partners
            # whose balance is 0
            params = (account_id.id, company_id, journal_ids, )
            if not allow_write_off:
                query = """
                    SELECT partner_id
                    FROM account_move_line
                    WHERE account_id=%s
                        AND reconcile_id IS NULL
                        AND state <> 'draft'
                        AND company_id = %s
                        AND journal_id IN %s
                    GROUP BY partner_id
                    HAVING ABS(SUM(debit-credit)) = 0.0
                        AND count(*)>0"""
            else:
                query = """
                    SELECT partner_id
                    FROM account_move_line
                    WHERE account_id=%s
                        AND reconcile_id IS NULL
                        AND state <> 'draft'
                        AND company_id = %s
                        AND journal_id IN %s
                    GROUP BY partner_id
                    HAVING ABS(SUM(debit-credit)) < %s
                        AND count(*)>0"""
                params += (max_amount,)
            cr.execute(query, params)
            id_list = cr.fetchall()
            partner_ids = [id for (id,) in id_list]
            for partner_id in partner_ids:
                if partner_id:
                    cr.execute("""
                        SELECT id
                        FROM account_move_line
                        WHERE account_id = %s
                            AND partner_id = %s
                            AND state <> 'draft'
                            AND reconcile_id IS NULL
                            AND company_id = %s
                            AND journal_id IN %s """, (
                        account_id.id, partner_id, company_id,
                        journal_ids, ))
                else:
                    cr.execute(
                        """SELECT id
                        FROM account_move_line
                        WHERE account_id = %s
                            AND partner_id is NULL
                            AND state <> 'draft'
                            AND reconcile_id IS NULL
                            AND company_id = %s
                            AND journal_id IN %s """,
                        (account_id.id, company_id, journal_ids, ))
                line_ids = [id for (id,) in cr.fetchall()]
                if line_ids:
                    reconciled += len(line_ids)
                    if allow_write_off:
                        move_line_obj.reconcile(
                            cr, uid, line_ids, 'auto', form.writeoff_acc_id.id,
                            form.period_id.id, form.journal_id.id, context)
                    else:
                        move_line_obj.reconcile_partial(
                            cr, uid, line_ids, 'manual', context=context)

            # try and reconcile moves based on their names
            # (very quick and useful for POS moves)
            params = (account_id.id, company_id, journal_ids, )
            if not allow_write_off:
                query = """
                    SELECT name
                    FROM account_move_line
                    WHERE account_id=%s
                        AND reconcile_id IS NULL
                        AND state <> 'draft'
                        AND company_id = %s
                        AND journal_id IN %s GROUP BY name
                    HAVING ABS(SUM(debit-credit)) = 0.0 AND count(*)>0"""
            else:
                query = """
                    SELECT name
                    FROM account_move_line
                    WHERE account_id=%s
                        AND reconcile_id IS NULL
                        AND state <> 'draft'
                        AND company_id = %s
                        AND journal_id IN %s GROUP BY name
                    HAVING ABS(SUM(debit-credit)) < %s AND count(*)>0"""
                params += (max_amount,)
            cr.execute(query, params)
            names = [name for (name, ) in cr.fetchall()]
            for name in names:
                cr.execute(
                    """SELECT id
                    FROM account_move_line
                    WHERE account_id = %s
                    AND name = %s
                    AND state <> 'draft'
                    AND reconcile_id IS NULL
                    AND company_id = %s
                    AND journal_id IN %s """,
                    (account_id.id, name, company_id, journal_ids, ))
                line_ids = [id for (id, ) in cr.fetchall()]
                if line_ids:
                    reconciled += len(line_ids)
                    if allow_write_off:
                        move_line_obj.reconcile(
                            cr, uid, line_ids, 'auto', form.writeoff_acc_id.id,
                            form.period_id.id, form.journal_id.id, context)
                    else:
                        move_line_obj.reconcile_partial(
                            cr, uid, line_ids, 'manual', context=context)

            # try and reconcile moves based on their reference
            # (very quick and useful for POS moves)
            params = (account_id.id, company_id, journal_ids, )
            if not allow_write_off:
                query = """
                    SELECT ref
                    FROM account_move_line
                    WHERE account_id=%s
                        AND reconcile_id IS NULL
                        AND state <> 'draft'
                        AND company_id = %s
                        AND journal_id IN %s
                    GROUP BY ref
                    HAVING ABS(SUM(debit-credit)) = 0.0 AND count(*)>0"""
            else:
                query = """
                    SELECT ref
                    FROM account_move_line
                    WHERE account_id=%s
                        AND reconcile_id IS NULL
                        AND state <> 'draft'
                        AND company_id = %s
                        AND journal_id IN %s
                    GROUP BY ref
                HAVING ABS(SUM(debit-credit)) < %s AND count(*)>0"""
                params += (max_amount,)
            cr.execute(query, params)
            names = [name for (name, ) in cr.fetchall()]
            for name in names:
                cr.execute("""
                    SELECT id
                    FROM account_move_line
                    WHERE account_id = %s
                        AND ref = %s
                        AND state <> 'draft'
                        AND reconcile_id IS NULL
                        AND company_id = %s
                        AND journal_id IN %s """, (
                    account_id.id, name,
                    company_id, journal_ids, ))
                line_ids = [id for (id, ) in cr.fetchall()]
                if line_ids:
                    reconciled += len(line_ids)
                    if allow_write_off:
                        move_line_obj.reconcile(
                            cr, uid, line_ids, 'auto', form.writeoff_acc_id.id,
                            form.period_id.id, form.journal_id.id, context)
                    else:
                        move_line_obj.reconcile_partial(
                            cr, uid, line_ids, 'manual', context=context)

            # get the list of partners who have more than
            # one unreconciled transaction
            cr.execute("""
                SELECT partner_id
                FROM account_move_line
                WHERE account_id=%s
                AND reconcile_id IS NULL
                AND state <> 'draft'
                AND company_id=%s
                GROUP BY partner_id
                HAVING count(*)>1""", (account_id.id, company_id))
            partner_ids = [id for (id,) in cr.fetchall()]

            for partner_id in partner_ids:
                if partner_id:
                    # get the list of unreconciled 'debit transactions'
                    # for this partner
                    cr.execute("""
                        SELECT id, debit
                        FROM account_move_line
                        WHERE account_id=%s
                            AND partner_id=%s
                            AND reconcile_id IS NULL
                            AND state <> 'draft'
                            AND debit > 0
                            AND company_id=%s
                        ORDER BY date_maturity""", (
                        account_id.id, partner_id, company_id))
                    debits = cr.fetchall()

                # get the list of unreconciled 'credit transactions'
                # for this partner
                    cr.execute("""
                        SELECT id, credit
                        FROM account_move_line
                        WHERE account_id=%s
                            AND partner_id=%s
                            AND reconcile_id IS NULL
                            AND state <> 'draft'
                            AND credit > 0
                            AND company_id=%s
                        ORDER BY date_maturity""", (
                        account_id.id, partner_id, company_id))
                    credits = cr.fetchall()
                else:  # manage case where partner_id is none (most pos moves)
                    cr.execute("""
                        SELECT id, debit
                        FROM account_move_line
                        WHERE account_id=%s
                        AND partner_id IS NULL
                        AND reconcile_id IS NULL
                        AND state <> 'draft'
                        AND debit > 0
                        AND company_id=%s
                        ORDER BY date_maturity""", (account_id.id, company_id))
                    debits = cr.fetchall()

                    cr.execute("""
                        SELECT id, credit
                        FROM account_move_line
                        WHERE account_id=%s
                            AND partner_id IS NULL
                            AND reconcile_id IS NULL
                            AND state <> 'draft'
                            AND credit > 0
                            AND company_id=%s
                        ORDER BY date_maturity""", (account_id.id, company_id))
                    credits = cr.fetchall()

                (rec, unrec) = self.do_reconcile(
                    cr, uid, credits, debits, max_amount, power,
                    form.writeoff_acc_id.id, form.period_id.id,
                    form.journal_id.id, context)
                reconciled += rec
                unreconciled += unrec

            # add the number of transactions for partners who have only one
            # unreconciled transactions to the unreconciled count
            partner_filter = (
                partner_ids and partner_ids[0] and
                'AND partner_id not in (%s)' % ','.join(
                    map(str, filter(None, partner_ids))) or '')
            cr.execute("""
                SELECT count(*)
                FROM account_move_line
                WHERE account_id=%s
                    AND reconcile_id IS NULL
                    AND company_id=%s
                    AND state <> 'draft' """ + partner_filter, (
                account_id.id, company_id,))
            additional_unrec = cr.fetchone()[0]
            unreconciled = unreconciled + additional_unrec
        context.update(
            {'reconciled': reconciled, 'unreconciled': unreconciled})
        model_data_ids = obj_model.search(
            cr, uid, [
                ('model', '=', 'ir.ui.view'),
                ('name', '=', 'account_automatic_reconcile_view1')])
        resource_id = obj_model.read(
            cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.automatic.reconcile',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }
