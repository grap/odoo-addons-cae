# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import string
from random import choice

from openerp.osv import fields
from openerp.osv.orm import TransientModel


class ResCompanyCreateWizard(TransientModel):
    _name = 'res.company.create.wizard'

    _PASSWORD_SIZE = 8

    _COMPANY_TYPE = [
        ('integrated', 'Integrated Company'),
        ('associated', 'Associated Company'),
        # TODO ('mother', 'Mother'),
    ]

    _columns = {
        'state': fields.selection(
            [('init', 'init'), ('pending', 'pending'), ('done', 'done')],
            'Status', readonly=True),
        'name': fields.char('Name', required=True, size=128),
        'mother_company': fields.many2one(
            'res.company', 'Mother Company', required=True,
            domain="[('fiscal_type', '!=', 'fiscal_child')]"),
        'company_id': fields.many2one(
            'res.company', 'Company'),
        'fiscal_company': fields.related(
            'company_id', 'fiscal_company', type='many2one',
            relation='res.company', string='Fiscal Company'),
        'vat': fields.char(
            'Tax ID', size=32),
        'type': fields.selection(
            _COMPANY_TYPE, 'Type', required=True),
        'code': fields.char(
            'Code', size=3, required=True,
            help="""This field is used as a prefix to generate automatic and"""
            """ unique reference for items (product, ...)."""
            """Warning, changing this value will change the reference of all"""
            """ items of this company.""",
        ),
        'password': fields.char(
            'Password', size=_PASSWORD_SIZE, readonly=True),
    }

    # Default Section
    _defaults = {
        'state': 'init',
    }

    # Constraint Section
    def _check_mother_company(self, cr, uid, ids, context=None):
        for rccw in self.browse(cr, uid, ids, context=context):
            if rccw.type == 'integrated':
                if rccw.mother_company.fiscal_type != 'fiscal_mother':
                    return False
            if rccw.type == 'associated':
                if (rccw.mother_company.fiscal_type != 'normal' or
                        rccw.mother_company.parent_id):
                    return False
        return True

    _constraints = [
        (
            _check_mother_company,
            """Error on Mother Company: Please select a normal Parent"""
            """ Company if the company is 'associated' and and a Fiscal"""
            """ Mother Company, if the company is 'integrated'""",
            ['type', 'mother_company']),
    ]

    # View Section
    def onchange_type_mother_company(
            self, cr, uid, ids, type, mother_company, context=None):
        """Overloadable function"""
        return {'value': {}}

    def button_begin(self, cr, uid, ids, context=None):
        id = ids[0]
        self.begin(cr, uid, id, context=context)
        self.write(cr, uid, [id], {
            'state': 'pending'}, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.company.create.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def button_finish(self, cr, uid, ids, context=None):
        id = ids[0]
        self.finish(cr, uid, id, context=context)
        self.write(cr, uid, [id], {
            'state': 'done'}, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.company.create.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    # Overloadable Function
    def res_company_values(self, cr, uid, id, context=None):
        return {}

    def res_users_values(self, cr, uid, id, context=None):
        return {
            'customer': False,
        }

    def res_groups_values(self, cr, uid, context=None):
        res = ['base.group_sale_manager']
        return res

    def begin(self, cr, uid, id, context=None):
        rccw = self.browse(cr, uid, id, context=context)
        rc_obj = self.pool['res.company']
        rg_obj = self.pool['res.groups']
        rp_obj = self.pool['res.partner']
        ru_obj = self.pool['res.users']
        imd_obj = self.pool['ir.model.data']
        # Create Company
        vals = self.res_company_values(cr, uid, id, context=context)
        vals.update({
            'name': rccw.name,
            'code': rccw.code,
            'parent_id': rccw.mother_company.id,
        })
        if rccw.type == 'integrated':
            vals['fiscal_type'] = 'fiscal_child'
            vals['fiscal_company'] = rccw.mother_company.id
            vals['rml_header'] = rccw.mother_company.rml_header
        else:
            vals['fiscal_type'] = 'normal'
            vals['fiscal_company'] = False
        rc_id = rc_obj.create(cr, uid, vals, context=context)

        # Set Current User to the new company
        ru_obj.write(cr, uid, [uid], {
            'company_id': rc_id,
            'company_ids': [(4, rc_id)],
            }, context=context)

        # Manage Extra Data in Partner associated
        vals = {'customer': False}
        if rccw.type == 'integrated':
            vals['vat'] = rccw.mother_company.vat
        else:
            vals['vat'] = rccw.vat
        rc = rc_obj.browse(cr, uid, rc_id, context=context)
        rp_obj.write(cr, uid, [rc.partner_id.id], vals, context=context)

        # Create Generic User
        characters = string.ascii_letters + string.digits
        password = "".join(choice(characters) for x in range(8))
        vals = self.res_users_values(cr, uid, id, context=context)

        vals.update({
            'name': rccw.name,
            'login': rccw.code,
            'new_password': password,
            'company_id': rc_id,
            'company_ids': [(4, rc_id)],
        })
        ru_id = ru_obj.create(cr, uid, vals, context=context)
        self.write(cr, uid, id, {
            'password': password,
            'company_id': rc_id,
        }, context=context)
        ru = ru_obj.browse(cr, uid, ru_id, context=context)

        # Add user to groups
        for group in self.res_groups_values(cr, uid, context=context):
            tab = group.split('.')
            rg_id = imd_obj.get_object_reference(cr, uid, tab[0], tab[1])[1]
            rg = rg_obj.browse(cr, uid, rg_id, context=context)
            users = [x.id for x in rg.users]
            users.append(ru.id)
            rg_obj.write(
                cr, uid, [rg_id], {'users': [[6, False, users]]},
                context=context)

        return {
            'company_id': rc_id,
            'user_id': ru_id,
            'partner_id': ru.partner_id,
        }

    def finish(self, cr, uid, id, context=None):
        return {}
