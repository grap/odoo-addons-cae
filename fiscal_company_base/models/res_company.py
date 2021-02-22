# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models

_RES_COMPANY_FISCAL_TYPE = [
    ("group", "Group"),
    ("normal", "Normal"),
    ("fiscal_mother", "CAE"),
    ("fiscal_child", "Integrated Company"),
]


class ResCompany(models.Model):
    _inherit = "res.company"
    _order = "fiscal_company_id, fiscal_type desc, name"

    # Columns Section
    fiscal_type = fields.Selection(
        selection=_RES_COMPANY_FISCAL_TYPE,
        string="Fiscal Type",
        required=True,
        default="normal",
    )

    fiscal_company_id = fields.Many2one(
        comodel_name="res.company", string="Fiscal Company"
    )

    fiscal_child_ids = fields.One2many(
        comodel_name="res.company",
        inverse_name="fiscal_company_id",
        string="Technical Integrated Companies",
        readonly=True,
    )

    other_fiscal_child_ids = fields.One2many(
        comodel_name="res.company",
        compute="_compute_other_fiscal_child_ids",
        string="Integrated Companies",
    )

    @api.multi
    def _compute_other_fiscal_child_ids(self):
        for company in self:
            companies = self.search(
                [("id", "in", company.fiscal_child_ids.ids), ("id", "!=", company.id)]
            )
            company.other_fiscal_child_ids = companies.ids

    # Constrains Section
    @api.constrains("fiscal_child_ids", "fiscal_type")
    def _check_non_fiscal_childs(self):
        for company in self:
            if company.fiscal_type != "fiscal_mother" and len(
                company.other_fiscal_child_ids
            ):
                raise exceptions.ValidationError(
                    _("Only CAE company can have Integrated Companies")
                )

    @api.constrains("fiscal_company_id", "fiscal_type")
    def _check_non_fiscal_child_company(self):
        for company in self:
            # skip special case of creation
            if company.fiscal_company_id:
                if (
                    company.fiscal_type in ("normal", "fiscal_mother")
                    and company.id != company.fiscal_company_id.id
                ):
                    raise exceptions.ValidationError(
                        _(
                            "You can't select in the field fiscal company, an"
                            " other company for a non integrated company."
                        )
                    )
                elif (
                    company.fiscal_type == "fiscal_child"
                    and company.fiscal_company_id.fiscal_type != "fiscal_mother"
                ):
                    raise exceptions.ValidationError(
                        _(
                            "You should select in the field fiscal company, a"
                            " CAE company for a Integrated Company."
                        )
                    )

    # Overload Section
    @api.model
    def create(self, vals):
        company = super().create(vals)
        if not vals.get("fiscal_company_id", False):
            company.fiscal_company_id = company.id
        if vals.get("fiscal_type", False) == "fiscal_child":
            company._propagate_access_right()
        return company

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if vals.get("fiscal_type", False) == "fiscal_child":
            self._propagate_access_right()
        return res

    # Private section
    @api.multi
    def _propagate_access_right(self):
        """Give access to the given fiscal child companies to all the
        users that have access to the fiscal mother company"""
        for company in self:
            user_ids = company.fiscal_company_id.user_ids.ids
            new_user_ids = list(set(user_ids) - set(company.user_ids.ids))
            company.write({"user_ids": [(4, id) for id in list(set(new_user_ids))]})
