# coding: utf-8
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class ResCompanyCreateWizard(models.TransientModel):
    _inherit = 'res.company.create.wizard'


    _FISCALYEAR_LAST_MONTH_SELECTION = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]

#    def _get_journal_ids(
#            self, cr, uid, ids, field_name, arg, context=None):
#        res = {}
#        aj_obj = self.pool['account.journal']
#        for rccw in self.browse(cr, uid, ids, context=context):
#            if rccw.company_id and rccw.type in ['associated']:
#                res[rccw.id] = aj_obj.search(cr, uid, [
#                    ('company_id', '=', rccw.company_id.id)], context=context)
#            else:
#                res[rccw.id] = []
#        return res

    # Columns Section
    chart_template_id = fields.Many2one(
        comodel_name='account.chart.template', string='Account Template',
        domain="[('visible', '=', True)]")

    fiscalyear_last_day = fields.Integer(
        string='Fiscal Year Last Day', default=31)

    fiscalyear_last_month = fields.Selection(
        string='Fiscal Year Last Month',  default=12,
        selection=_FISCALYEAR_LAST_MONTH_SELECTION)

    sale_tax_template_id = fields.Many2one(
        comodel_name='account.tax.template', string='Default sale tax',
        domain="["
        "('chart_template_id', '=', chart_template_id),"
        "('parent_id','=',False),"
        "('type_tax_use','in', ('sale', 'all'))]")

    purchase_tax_template_id = fields.Many2one(
        comodel_name='account.tax.template', string='Default purchase tax',
        domain="["
        "('chart_template_id', '=', chart_template_id),"
        "('parent_id','=',False),"
        "('type_tax_use','in', ('purchase', 'all'))]")

#    'journal_ids': fields.function(
#        _get_journal_ids, 'Journals', type='one2many',
#        relation='account.journal'),
#    'account_receivable_id': fields.many2one(
#        'account.account', 'Account Receivable',
#        domain="[('company_id', '=', fiscal_company),"
#        "('type', '=', 'receivable')]"),
#    'account_payable_id': fields.many2one(
#        'account.account', 'Account Payable',
#        domain="[('company_id', '=', fiscal_company),"
#        "('type', '=', 'payable')]"),

#     transfer_account_id = fields.Many2one('account.account',
#        domain=lambda self: [('reconcile', '=', True), ('user_type_id.id', '=', self.env.ref('account.data_account_type_current_assets').id), ('deprecated', '=', False)], string="Inter-Banks Transfer Account", help="Intermediary account used when moving money from a liquidity account to another")

#    'category_line_ids': fields.one2many(
#        'res.company.create.wizard.category', 'wizard_id', 'Categories'),
#    }

#    # Default Section
#    # Fields Function Section
#    def _default_category_line_ids(self, cr, uid, context=None):
#        res = []
#        pc_obj = self.pool['product.category']
#        pc_ids = pc_obj.search(cr, uid, [
#            ('parent_id', '=', False)], context=context)
#        for pc_id in pc_ids:
#            res.append((0, 0, {
#                'category_id': pc_id,
#                'income_account_id': False,
#                'expense_account_id': False,
#            }))
#        return res

#    _defaults = {
#        'date_start': lambda *a: time.strftime('%Y-%m-01'),
#        'date_stop': lambda *a: time.strftime('%Y-12-31'),
#        'category_line_ids': _default_category_line_ids,
#    }


    @api.multi
    def _prepare_user_groups(self):
        """Overload this function. Should return a list of xml ids of groups"""
        self.ensure_one()
        res = super(ResCompanyCreateWizard, self)._prepare_user_groups()
        res.append('account.group_account_user')
        return res

#    def res_company_values(self, cr, uid, id, context=None):
#        res = super(res_company_create_wizard, self).res_company_values(
#            cr, uid, id, context=context)
#        rccw = self.browse(cr, uid, id, context=context)
#        res.update({
#            'expects_chart_of_accounts': rccw.type in ['associated'],
#        })
#        return res

    @api.multi
    def begin(self):
        self.ensure_one()
        char_wizard_obj = self.env['wizard.multi.charts.accounts']
        res = super(ResCompanyCreateWizard, self).begin()

        # Install Chart of Accounts
        if self.fiscal_type != 'fiscal_child':
#            
            chart_wizard = chart_wizard_obj.create({
                'company_id': self.company_id.id,
                'chart_template_id': self.chart_template_id.id,
                'code_digits': rccw.code_digits,
                'sale_tax': rccw.sale_tax.id,
                'sale_tax_rate': rccw.sale_tax_rate,
                'purchase_tax': rccw.purchase_tax.id,
                'purchase_tax_rate': rccw.purchase_tax_rate,
                'complete_tax_set': rccw.chart_template_id.complete_tax_set,
                'currency_id': rccw.company_id.currency_id.id,
            }, context)
            wmca_obj.execute(cr, uid, [wmca_id], context)

#            ip_payable_id = ip_obj.search(cr, uid, [
#                ('name', '=', 'property_account_payable'),
#                ('company_id', '=', rccw.company_id.id)],
#                context=context)
#            ip_payable = ip_obj.browse(
#                cr, uid, ip_payable_id[0], context=context)
#            ip_receivable_id = ip_obj.search(cr, uid, [
#                ('name', '=', 'property_account_receivable'),
#                ('company_id', '=', rccw.company_id.id)],
#                context=context)
#            ip_receivable = ip_obj.browse(
#                cr, uid, ip_receivable_id[0], context=context)
#            self.write(cr, uid, rccw.id, {
#                'account_receivable_id': ip_receivable.value_reference.id,
#                'account_payable_id': ip_payable.value_reference.id,
#            }, context=context)

#            # We drop some useless properties created by the function
#            # wizard_multi_charts_accounts::generate_properties
#            to_drop = [
#                'property_account_expense_categ',
#                'property_account_income_categ',
#                'property_account_expense',
#                'property_account_income',
#                'property_account_payable',
#                'property_account_receivable',
#            ]
#            ip_ids = ip_obj.search(cr, uid, [
#                ('name', 'in', to_drop),
#                ('company_id', '=', rccw.company_id.id)],
#                context=context)
#            ip_obj.unlink(cr, uid, ip_ids, context=context)

#            # Create Fiscal Year and Period
#            name = code = rccw.date_start[:4]
#            if int(name) != int(rccw.date_stop[:4]):
#                name = rccw.date_start[:4] + '-' + rccw.date_stop[:4]
#                code = rccw.date_start[-2:] + '-' + rccw.date_stop[-2:]
#            vals = {
#                'name': name,
#                'code': code,
#                'date_start': rccw.date_start,
#                'date_stop': rccw.date_stop,
#                'company_id': rccw.company_id.id,
#            }
#            afy_id = afy_obj.create(cr, uid, vals, context=context)
#            afy_obj.create_period(cr, uid, [afy_id], context=context)

#        res.update({
#            'payment_term_id': payment_term_id,
#        })
#        return res

#        imd_obj = self.pool['ir.model.data']
#        ip_obj = self.pool['ir.property']
#        afy_obj = self.pool['account.fiscalyear']

#        rccw = self.browse(cr, uid, id, context=context)

#        # Define Payment Term. (Static for the moment)
#        payment_term_id = imd_obj.get_object_reference(
#            cr, uid, 'account', 'account_payment_term_immediate')[1]

#    def finish(self, cr, uid, id, context=None):
#        ip_obj = self.pool['ir.property']
#        imd_obj = self.pool['ir.model.data']
#        rccw = self.browse(cr, uid, id, context=context)

#        res = super(res_company_create_wizard, self).finish(
#            cr, uid, id, context=context)

#        # Create Default Properties
#        ip_obj.create(cr, uid, {
#            'name': 'property_account_receivable',
#            'company_id': rccw.company_id.id,
#            'fields_id': imd_obj.get_object_reference(
#                cr, uid, 'account',
#                'field_res_partner_property_account_receivable')[1],
#            'type': 'many2one',
#            'value_reference': 'account.account,%s' % (
#                rccw.account_receivable_id.id),
#        }, context=context)

#        ip_obj.create(cr, uid, {
#            'name': 'property_account_payable',
#            'company_id': rccw.company_id.id,
#            'fields_id': imd_obj.get_object_reference(
#                cr, uid, 'account',
#                'field_res_partner_property_account_payable')[1],
#            'type': 'many2one',
#            'value_reference': 'account.account,%s' % (
#                rccw.account_payable_id.id),
#        }, context=context)

#        pc_obj = self.pool['product.category']
#        if rccw.type in ('associated'):
#            # create Expense / Income Properties
#            for category_line in rccw.category_line_ids:
#                expense_id = category_line.expense_account_id\
#                    and category_line.expense_account_id.id or False
#                income_id = category_line.income_account_id.id\
#                    and category_line.income_account_id.id or False
#                pc_obj.write(cr, uid, [category_line.category_id.id], {
#                    'property_account_expense_categ': expense_id,
#                    'property_account_income_categ': income_id,
#                    }, context=context)
#        return res

#    # View Section
#    def onchange_chart_template_id(
#            self, cr, uid, ids, chart_template_id, context=None):
#        tax_templ_obj = self.pool['account.tax.template']
#        res = {'value': {
#            'complete_tax_set': False,
#            'sale_tax': False,
#            'purchase_tax': False,
#            'sale_tax_rate': 0,
#            'purchase_tax_rate': 0,
#        }}
#        if chart_template_id:
#            # update complete_tax_set, sale_tax and purchase_tax
#            chart_template = self.pool['account.chart.template'].browse(
#                cr, uid, chart_template_id, context=context)
#            res['value'].update(
#                {'complete_tax_set': chart_template.complete_tax_set})
#            if chart_template.complete_tax_set:
#                sale_tax_ids = tax_templ_obj.search(
#                    cr, uid, [
#                        ("chart_template_id", "=", chart_template_id),
#                        ('type_tax_use', 'in', ('sale', 'all'))],
#                    order="sequence, id desc")
#                purchase_tax_ids = tax_templ_obj.search(
#                    cr, uid, [
#                        ("chart_template_id", "=", chart_template_id),
#                        ('type_tax_use', 'in', ('purchase', 'all'))],
#                    order="sequence, id desc")
#                res['value']['sale_tax'] = \
#                    sale_tax_ids and sale_tax_ids[0] or False
#                res['value']['purchase_tax'] = \
#                    purchase_tax_ids and purchase_tax_ids[0] or False
#            if chart_template.code_digits:
#                res['value']['code_digits'] = chart_template.code_digits
#        return res
