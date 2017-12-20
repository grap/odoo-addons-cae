# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from openerp import SUPERUSER_ID
from openerp.osv import fields
from openerp.osv.orm import Model

_DEFAULT_COMPANY_CODE = 'ZZZ'


class ResCompany(Model):
    _inherit = 'res.company'

    _RES_COMPANY_FISCAL_TYPE = [
        ('normal', 'Normal'),
        ('fiscal_mother', 'Fiscal Mother Company'),
        ('fiscal_child', 'Fiscal Child Company'),
    ]

    # Private function section
    def _propagate_access_right(self, cr, uid, ids, context=None):
        args = [('id', 'in', ids), ('fiscal_type', '=', 'fiscal_child')]
        rc_ids = self.search(cr, uid, args, context=context)
        for rc in self.browse(cr, uid, rc_ids, context=context):
            ru_ids = [ru.id for ru in rc.fiscal_company.user_ids]
            ru_new_ids = list(set(ru_ids) - set(rc.user_ids))
            self.write(cr, uid, [rc.id], {
                'user_ids': [(4, id) for id in list(set(ru_new_ids))]},
                context=context)

    # Columns Section
    _columns = {
        'administrative_department_email': fields.char(
            string='Administrative Department Email'),
        'fiscal_type': fields.selection(
            _RES_COMPANY_FISCAL_TYPE,
            string='Fiscal Type', required=True),
        'fiscal_company': fields.many2one(
            'res.company', 'Fiscal Company'),
        'fiscal_childs': fields.one2many(
            'res.company', 'fiscal_company', string='Fiscal Childs',
            readonly=True),
        'code': fields.char(
            string='Code', size=3,
            help="""This field is used as a prefix to generate automatic and"""
            """ unique reference for items (product, ...).\n"""
            """Warning, changing this value will change the reference of all"""
            """ items of this company.""",
        ),
    }

    _defaults = {
        'code': _DEFAULT_COMPANY_CODE,
        'fiscal_type': 'normal',
    }

    # Constraint Section
    def _check_non_fiscal_child_company(self, cr, uid, ids, context=None):
        for rc in self.browse(cr, uid, ids, context=context):
            # skip special case of creation
            if rc.fiscal_company:
                if (rc.fiscal_type in ('normal', 'fiscal_mother') and
                        rc.id != rc.fiscal_company.id):
                    return False
        return True

    def _check_fiscal_mother_company(self, cr, uid, ids, context=None):
        for rc in self.browse(cr, uid, ids, context=context):
            # skip special case of creation
            if rc.fiscal_company is not None:
                if (rc.fiscal_type == 'fiscal_child' and
                        rc.fiscal_company.fiscal_type != 'fiscal_mother'):
                    return False
        return True

    _constraints = [
        (_check_non_fiscal_child_company,
            "You can't select an other company for a Non Fiscal Child Company",
            ['fiscal_company', 'fiscal_type']),
        (_check_fiscal_mother_company,
            "Please select a Fiscal Mother Company for a Fiscal Child Company",
            ['fiscal_company', 'fiscal_type']),
    ]

    # Overload Section
    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False):
        """Add a required modifiers on the field code"""
        res = super(ResCompany, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar)
        if view_type in ('form', 'tree')\
                and 'code' in res['fields']:
            res['fields']['code']['required'] = True
            doc = etree.XML(res['arch'])
            node = doc.xpath("//field[@name='code']")[0]
            node.set('modifiers', '{"required": true}')
            res['arch'] = etree.tostring(doc)
        return res

    def create(self, cr, uid, vals, context=None):
        # TODO: FIXME when trunk will be fixed.
        # For the time being, it's not possible to create a company if
        # the user is not SUPERUSER_ID
        res = super(ResCompany, self).create(
            cr, SUPERUSER_ID, vals, context=context)
        if not vals.get('fiscal_company', False):
            self.write(cr, uid, [res], {
                'fiscal_company': res}, context=context)
        elif vals.get('fiscal_type', False) == 'fiscal_child':
            self._propagate_access_right(
                cr, uid, [res], context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ResCompany, self).write(
            cr, uid, ids, vals, context=context)
        if vals.get('fiscal_company', False):
            self._propagate_access_right(cr, uid, ids, context=context)
        return res
