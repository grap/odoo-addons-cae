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
        user = super().create(vals)
        if vals.get('company_ids', False):
            user._propagate_access_right()
        return user

    @api.multi
    def write(self, vals):
        res = super().write(vals)
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
            for mother_company in user.company_ids.filtered(
                    lambda x: x.fiscal_type == 'fiscal_mother'):
                all_ids = mother_company.fiscal_child_ids.ids
                existing_ids = user.company_ids.ids
                new_company_ids += (list(set(all_ids) - set(existing_ids)))
            super(ResUsers, user).write({
                'company_ids': [(4, id) for id in list(set(new_company_ids))]})
