# coding: utf-8
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# flake8: noqa

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

    code_digits = fields.Integer(string='# of Digits')

    fiscalyear_last_day = fields.Integer(
        string='Fiscal Year Last Day', default=31)

    fiscalyear_last_month = fields.Selection(
        string='Fiscal Year Last Month',  default=12,
        selection=_FISCALYEAR_LAST_MONTH_SELECTION)

    payable_account_template_id = fields.Many2one(
        comodel_name='account.account.template',
        string='Default Payable Account',
        domain= lambda s: s._get_account_template_domain('payable'))

    receivable_account_template_id = fields.Many2one(
        comodel_name='account.account.template',
        string='Default Receivable Account',
        domain= lambda s: s._get_account_template_domain('receivable'))
#        domain="["
#        "('chart_template_id', '=', chart_template_id),"
#        "('reconcile','=', True)]")

    @api.model
    def _get_account_template_domain(self, type_name):
        if type_name == 'current_assets':
            type = self.env.ref('account.data_account_type_current_assets')
        elif type_name == 'receivable':
            type = self.env.ref('account.data_account_type_receivable')
        elif type_name == 'payable':
            type = self.env.ref('account.data_account_type_payable')
        return [('user_type_id', '=', type.id)]

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
    def _prepare_chart_wizard(self):
        self.ensure_one()
        return {
            'company_id': self.company_id.id,
            'chart_template_id': self.chart_template_id.id,
            'code_digits': self.code_digits,
            'sale_tax_id': False,
            'purchase_tax_id': False,
        }

    @api.multi
    def _begin(self):
        self.ensure_one()
        char_wizard_obj = self.env['wizard.multi.charts.accounts']
        res = super(ResCompanyCreateWizard, self)._begin()

        if self.fiscal_type != 'fiscal_child':
            # Install Chart of Accounts
            chart_wizard = chart_wizard_obj.create(self._prepare_chart_wizard)
            chart_wizard.execute()

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
    @api.onchange('chart_template_id')
    def onchange_chart_template_id(self):
        if self.chart_template_id:
            self.code_digits = self.chart_template_id.code_digits


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
