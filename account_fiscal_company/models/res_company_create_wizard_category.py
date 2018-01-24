# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv import fields
from openerp.osv.orm import TransientModel


class ResCompanyCreateWizardCategory(TransientModel):
    _name = 'res.company.create.wizard.category'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'res.company.create.wizard', 'Wizard'),
        'company_id': fields.related(
            'wizard_id', 'company_id', type='many2one',
            string='Company', relation='res.company'),
        'category_id': fields.many2one(
            'product.category', 'Category'),
        'expense_account_id': fields.many2one(
            'account.account', 'Expense Account',
            domain="[('company_id', '=', company_id),"
            "('type', '=', 'other')]"),
        'income_account_id': fields.many2one(
            'account.account', 'Income Account',
            domain="[('company_id', '=', company_id),"
            "('type', '=', 'other')]"),
    }
