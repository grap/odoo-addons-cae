# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class ConsignorCreateWizard(models.TransientModel):
    _inherit = "consignor.create.wizard"

    @api.multi
    def _prepare_account(self):
        res = super()._prepare_account()
        res.update(
            {
                "company_id": self.env.user.company_id.fiscal_company_id.id,
            }
        )
        return res

    @api.multi
    def _prepare_tax(self, sequence, account, partner, commission_product):
        res = super()._prepare_tax(sequence, account, partner, commission_product)
        res.update(
            {
                "company_id": self.env.user.company_id.fiscal_company_id.id,
            }
        )
        return res
