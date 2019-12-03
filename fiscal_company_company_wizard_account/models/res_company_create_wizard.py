# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import Warning as UserError


class ResCompanyCreateWizard(models.TransientModel):
    _inherit = 'res.company.create.wizard'

    # Onchange Section
    @api.onchange('fiscal_type')
    def onchange_fiscal_type(self):
        res = super().onchange_fiscal_type()
        if self.fiscal_type == 'fiscal_child':
            self.chart_template_id = False
        return res

    @api.constrains('fiscal_type', 'chart_template_id')
    def _check_onchange_fiscal_type_chart_template(self):
        for wizard in self:
            if wizard.fiscal_type == 'fiscal_child'\
                    and wizard.chart_template_id:
                raise UserError(_(
                    "You can not select a Chart of Account for a Fiscal Child"
                    " Company"))
            elif wizard.fiscal_type == 'fiscal_mother'\
                    and not wizard.chart_template_id:
                raise UserError(_(
                    "You have to select a Chart of Account for a Fiscal Mother"
                    " Company"))
