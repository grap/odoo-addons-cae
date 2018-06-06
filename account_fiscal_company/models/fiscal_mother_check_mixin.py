# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, models
from openerp.exceptions import Warning as UserError


class FiscalMotherCheckMixin(models.AbstractModel):
    _name = 'fiscal.mother.check.mixin'

    @api.constrains('company_id')
    def _check_fiscal_mother_company_id(self):
        for item in self:
            if item.company_id.fiscal_type == 'fiscal_mother':
                raise UserError(_(
                    "FROMaGE !"
                    "You can't affect this item to a fiscal mother company."))
