# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_RES_COMPANY_FISCAL_TYPE = [
    ("group", "Group"),
    ("normal", "Associate Company"),
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

    def _get_fiscal_propagated_fields(self):
        """Return list of company fields that should be propagated to the
        child companies"""
        return ["vat"]

    def _get_model_from_properties_propagation(self):
        """Return list of models that inherit from
        fiscal.company.propagate.child.company.mixin
        and that should propagate properties to child companies.
        """
        return ["res.partner"]

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        for company, vals in zip(companies, vals_list, strict=True):
            if vals.get("fiscal_type") == "fiscal_child":
                company._propagate_properties_to_new_fiscal_child()
        return companies

    def write(self, vals):
        res = super().write(vals)
        cae_companies = self.filtered(lambda x: x.fiscal_type == "fiscal_mother")

        if vals.get("fiscal_type") == "fiscal_child":
            self._propagate_properties_to_new_fiscal_child()

        new_vals = {}

        for field in self._get_fiscal_propagated_fields():
            if field in vals.keys():
                new_vals[field] = vals[field]

        if new_vals and cae_companies:
            super(ResCompany, cae_companies.mapped("child_ids")).write(new_vals)

        return res

    @api.onchange("parent_id")
    def _onchange_parent_id_fiscal_propagated_fields(self):
        if self.parent_id.fiscal_type == "fiscal_mother":
            for field in self._get_fiscal_propagated_fields():
                parent_value = getattr(self.parent_id, field)
                if parent_value:
                    setattr(self, field, parent_value)

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

    def _propagate_properties_to_new_fiscal_child(self):
        """
        Propagate all properties of some models for a new child company
        """
        IrModelFields = self.env["ir.model.fields"]
        IrProperty = self.env["ir.property"]
        for company in self:
            for model_name in self._get_model_from_properties_propagation():
                CurrentModel = self.env[model_name]
                property_name_list = CurrentModel._fiscal_property_creation_list()
                for property_name in property_name_list:
                    field = IrModelFields.search(
                        [("model", "=", model_name), ("name", "=", property_name)]
                    )[0]
                    # Get existing properties
                    existing_properties = IrProperty.sudo().search(
                        [
                            ("fields_id", "=", field.id),
                            ("company_id", "=", company.fiscal_company_id.id),
                        ]
                    )
                    # Duplicate properties for the new fiscal child company
                    for existing_property in existing_properties:
                        existing_property.copy(default={"company_id": company.id})
