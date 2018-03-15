# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Columns Section
    administrative_ok = fields.Boolean(
        string='Is Administrative',
        help="If checked, this product will be readonly for users and"
        " updatable only by specific group")

    # Overload Section
    @api.model
    def create(self, vals):
        if vals.get('administrative_ok', False):
            self._check_administrative_access()
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('administrative_ok', False) or\
                any(self.mapped('administrative_ok')):
            self._check_administrative_access()
        return super(ProductTemplate, self).write(vals)

    @api.multi
    def unlink(self):
        if any(self.mapped('administrative_ok')):
            self._check_administrative_access()
        return super(ProductTemplate, self).unlink()

    # Custom Section
    @api.model
    def _check_administrative_access(self):
        if not self.env.user.has_group(
                'base_fiscal_company.res_group_administrative_manager'):
            raise UserError(_(
                "You have no right to create or update an"
                " administrative product"))
