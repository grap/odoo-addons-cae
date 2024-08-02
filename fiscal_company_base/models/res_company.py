# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_RES_COMPANY_FISCAL_TYPE = [
    ("group", "Group"),
    ("normal", "Normal"),
    ("fiscal_mother", "CAE"),
    ("fiscal_child", "Integrated Company"),
]


class ResCompany(models.Model):
    _inherit = "res.company"

    fiscal_type = fields.Selection(
        selection=_RES_COMPANY_FISCAL_TYPE,
        required=True,
        default="normal",
    )

    fiscal_company_id = fields.Many2one(
        comodel_name="res.company",
        string="Fiscal Company",
        compute="_compute_fiscal_company_id",
        store=True,
    )

    fiscal_child_ids = fields.One2many(
        comodel_name="res.company",
        inverse_name="fiscal_company_id",
        string="Technical Integrated Companies",
        readonly=True,
    )

    @api.depends("fiscal_type", "parent_id")
    def _compute_fiscal_company_id(self):
        for company in self:
            if company.fiscal_type in ["normal", "fiscal_mother"]:
                company.fiscal_company_id = company
            elif company.fiscal_type == "fiscal_child":
                company.fiscal_company_id = company.parent_id
            elif company.fiscal_type == "group":
                company.fiscal_company_id = False

    # Constrains Section
    @api.constrains("parent_id", "fiscal_type")
    def _check_fiscal_type_with_parent_type(self):
        for company in self.filtered(
            lambda x: x.fiscal_type in ["group", "normal", "fiscal_mother"]
        ):
            if company.parent_id.fiscal_type not in ["group", False]:
                raise ValidationError(
                    _(
                        "The company '%(company_name)s' (type %(fiscal_type_name)s)"
                        " can only have a parent company with a type 'Group'.",
                        company_name=company.name,
                        fiscal_type_name=company.fiscal_type,
                    )
                )
        for company in self.filtered(lambda x: x.fiscal_type in ["fiscal_child"]):
            if company.parent_id.fiscal_type != "fiscal_mother":
                raise ValidationError(
                    _(
                        "The company '%(company_name)s' (type 'Fiscal Child')"
                        " can only have a parent company with a type 'Fiscal Mother'.",
                        company_name=company.name,
                    )
                )

    @api.constrains("child_ids", "fiscal_type")
    def _check_fiscal_type_with_child_type(self):
        for company in self.filtered(
            lambda x: x.fiscal_type in ["normal", "fiscal_child"]
        ):
            if company.child_ids:
                raise ValidationError(
                    _(
                        "The company '%(company_name)s' can not be '%(fiscal_type)s'"
                        " because it contains companies.",
                        company_name=company.name,
                        fiscal_type=company.fiscal_type,
                    )
                )

        for company in self.filtered(lambda x: x.fiscal_type in ["fiscal_mother"]):
            error_types = set(company.mapped("child_ids.fiscal_type")) - set(
                {"fiscal_child"}
            )

            if error_types:
                raise ValidationError(
                    _(
                        "The company '%(company_name)s' can not be 'Fiscal Mother'"
                        " because it contains companies type of '%(error_types)s'",
                        company_name=company.name,
                        error_types=error_types,
                    )
                )

        for company in self.filtered(lambda x: x.fiscal_type in ["group"]):
            error_types = set(company.mapped("child_ids.fiscal_type")) - set(
                {"normal", "group", "fiscal_mother"}
            )

            if error_types:
                raise ValidationError(
                    _(
                        "The company '%(company_name)s' can not be 'Group'"
                        " because it contains companies type of '%(error_types)s'",
                        company_name=company.name,
                        error_types=error_types,
                    )
                )
