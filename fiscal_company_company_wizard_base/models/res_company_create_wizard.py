# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.fiscal_company_base.models.res_company import _RES_COMPANY_FISCAL_TYPE


class ResCompanyCreateWizard(models.TransientModel):
    _inherit = "res.company.create.wizard"

    fiscal_type = fields.Selection(
        selection=_RES_COMPANY_FISCAL_TYPE,
        string="Fiscal Type",
        required=True,
        default="normal",
    )

    @api.constrains("fiscal_type", "parent_company_id")
    def _check_fiscal_type_parent_company(self):
        res = self.filtered(
            lambda x: x.fiscal_type == "fiscal_child" and not x.parent_company_id
        )
        if res:
            raise ValidationError(
                _(
                    "you have to set a parent company if you create a new fiscal"
                    " child company"
                )
            )

    # Onchange Section
    @api.onchange("fiscal_type")
    def onchange_fiscal_type(self):
        domain_type_list = []
        if self.fiscal_type in ["normal", "fiscal_mother"]:
            domain_type_list = ["group"]
        elif self.fiscal_type == "fiscal_child":
            domain_type_list = ["fiscal_mother"]
            self.vat = False
        if (
            self.parent_company_id
            and self.parent_company_id.fiscal_type not in domain_type_list
        ):
            self.parent_company_id = False
        return {
            "domain": {"parent_company_id": [("fiscal_type", "in", domain_type_list)]}
        }

    @api.multi
    def _prepare_company(self):
        self.ensure_one()
        vals = super()._prepare_company()
        if self.fiscal_type == "fiscal_child":
            # Poor hack, to avoid error when creating directly fiscal child
            # company.
            # In V12, if we try to create a new GRAP child company
            # the system will try to recompute the value of the field
            # account.voucher company_id. (related field) for a bad reason.
            # TODO: VX: check if it is still mandatory.
            vals.update({})
        else:
            vals.update({"fiscal_type": self.fiscal_type})
        return vals

    @api.multi
    def _post_create_company(self):
        self.ensure_one()
        super()._post_create_company()
        if self.fiscal_type == "fiscal_child":
            self.company_id.write(
                {
                    "fiscal_type": self.fiscal_type,
                    "fiscal_company_id": self.parent_company_id.id,
                }
            )
