# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Columns Section
    cae_administrative_ok = fields.Boolean(
        string='Is CAE Administrative',
        help="If checked, this product will be readonly for users and"
        " updatable only by specific group")

    # Overload Section
    @api.model
    def create(self, vals):
        if vals.get('cae_administrative_ok', False):
            self._check_administrative_access()
        return super().create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('cae_administrative_ok', False) or\
                any(self.mapped('cae_administrative_ok')):
            self._check_administrative_access()
        return super().write(vals)

    @api.multi
    def unlink(self):
        if any(self.mapped('cae_administrative_ok')):
            self._check_administrative_access()
        return super().unlink()

    # Custom Section
    @api.model
    def _check_administrative_access(self):
        if not self.env.user.has_group(
                'fiscal_company_base.fiscal_company_manager'):
            raise ValidationError(_(
                "You have no right to create or update an"
                " administrative product"))
