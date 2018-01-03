# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Overload Section
    @api.model
    def create(self, vals):
        user = super(ResUsers, self).create(vals)
        if vals.get('company_ids', False):
            user._propagate_access_right()
        return user

    @api.multi
    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if vals.get('company_ids', False):
            self._propagate_access_right()
        return res

    # Private function section
    @api.multi
    def _propagate_access_right(self):
        """If a user has access to a fiscal_mother company, so he'll have
        access to all the child_company"""
        new_company_ids = []
        for user in self:
            for rc in user.company_ids:
                if rc.fiscal_type == 'fiscal_mother':
                    rc_all_ids = [
                        x.id for x in rc.fiscal_company.fiscal_childs]
                    rc_existing_ids = [
                        x.id for x in user.company_ids]
                    new_company_ids += (
                        list(set(rc_all_ids) - set(rc_existing_ids)))
            super(ResUsers, user).write({
                'company_ids': [(4, id) for id in list(set(new_company_ids))]})
