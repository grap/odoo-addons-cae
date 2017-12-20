# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class ResUsers(Model):
    _inherit = 'res.users'

    # Private function section
    def _propagate_access_right(self, cr, uid, ids, context=None):
        """If a user has access to a fiscal_mother company, so he'll have
        access to all the child_company"""
        rc_new_ids = []
        for ru in self.browse(cr, uid, ids, context=context):
            for rc in ru.company_ids:
                if rc.fiscal_type == 'fiscal_mother':
                    rc_all_ids = [
                        x.id for x in rc.fiscal_company.fiscal_childs]
                    rc_existing_ids = [
                        x.id for x in ru.company_ids]
                    rc_new_ids += (
                        list(set(rc_all_ids) - set(rc_existing_ids)))
            super(ResUsers, self).write(cr, uid, [ru.id], {
                'company_ids': [(4, id) for id in list(set(rc_new_ids))]},
                context=context)

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        user_id = super(ResUsers, self).create(cr, uid, vals, context=context)
        if vals.get('company_ids', False):
            self._propagate_access_right(cr, uid, [user_id], context=context)
        return user_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ResUsers, self).write(cr, uid, ids, vals, context=context)
        if vals.get('company_ids', False):
            self._propagate_access_right(cr, uid, ids, context=context)
        return res
