# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo import api, fields, models



class ResCompany(models.Model):
    _inherit = 'res.company'

    _RES_COMPANY_FISCAL_TYPE = [
        ('normal', 'Normal'),
        ('fiscal_mother', 'Fiscal Mother Company'),
        ('fiscal_child', 'Fiscal Child Company'),
    ]

    # Columns Section
    fiscal_type = fields.Selection(
        selection=_RES_COMPANY_FISCAL_TYPE, string='Fiscal Type',
        required=True, default='normal')

    fiscal_company = fields.Many2one(
        comodel_name='res.company', string='Fiscal Company')

    fiscal_childs = fields.One2many(
        comodel_name='res.company', inverse_name='fiscal_company',
        string='Fiscal Childs', readonly=True)

    code = fields.Char(
        string='Code', size=3,
        help="""This field is used as a prefix to generate automatic and"""
        """ unique reference for items (product, ...).\n"""
        """Warning, changing this value will change the reference of all"""
        """ items of this company.""",
    )

#    # Constraint Section
#    @api.constrains('fiscal_company', 'fiscal_type')
#    def _check_non_fiscal_child_company(self, cr, uid, ids, context=None):
#        for rc in self.browse(cr, uid, ids, context=context):
#            # skip special case of creation
#            if rc.fiscal_company:
#                if (rc.fiscal_type in ('normal', 'fiscal_mother') and
#                        rc.id != rc.fiscal_company.id):
#                    return False
#        return True

#    @api.constrains('fiscal_company', 'fiscal_type')
#    def _check_fiscal_mother_company(self, cr, uid, ids, context=None):
#        for rc in self.browse(cr, uid, ids, context=context):
#            # skip special case of creation
#            if rc.fiscal_company is not None:
#                if (rc.fiscal_type == 'fiscal_child' and
#                        rc.fiscal_company.fiscal_type != 'fiscal_mother'):
#                    return False
#        return True

#    _constraints = [
#        (_check_non_fiscal_child_company,
#            "You can't select an other company for a Non Fiscal Child Company",
#            []),
#        (_check_fiscal_mother_company,
#            "Please select a Fiscal Mother Company for a Fiscal Child Company",
#            []),
#    ]

#    # Overload Section
#    def fields_view_get(
#            self, cr, uid, view_id=None, view_type='form', context=None,
#            toolbar=False):
#        """Add a required modifiers on the field code"""
#        res = super(ResCompany, self).fields_view_get(
#            cr, uid, view_id=view_id, view_type=view_type, context=context,
#            toolbar=toolbar)
#        if view_type in ('form', 'tree')\
#                and 'code' in res['fields']:
#            res['fields']['code']['required'] = True
#            doc = etree.XML(res['arch'])
#            node = doc.xpath("//field[@name='code']")[0]
#            node.set('modifiers', '{"required": true}')
#            res['arch'] = etree.tostring(doc)
#        return res

    # Overload Section
    @api.model
    def create(self, vals):
        company = super(ResCompany, self).create(vals)
        if not vals.get('fiscal_company', False):
            company.fiscal_company = company.id
        elif vals.get('fiscal_type', False) == 'fiscal_child':
            company._propagate_access_right()
        return res

    @api.multi
    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        if vals.get('fiscal_company', False):
            self._propagate_access_right()
        return res

    # Private section
    @api.multi
    def _propagate_access_right(self):
        args = [('id', 'in', self.ids), ('fiscal_type', '=', 'fiscal_child')]
        companies = self.search(args)
        for company in companies:
            user_ids = company.fiscal_company.user_ids.ids
            new_user_ids = list(set(user_ids) - set(company.user_ids))
            company.write({
                'user_ids': [(4, id) for id in list(set(new_user_ids))]})
