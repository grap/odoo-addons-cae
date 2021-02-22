# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = "product.category"

    global_property_account_expense_categ = fields.Char(string="Expense Account Code")

    global_property_account_income_categ = fields.Char(string="Income Account Code")

    @api.model
    def create(self, vals):
        category = super().create(vals)
        field_names = []
        if vals.get("global_property_account_expense_categ"):
            field_names.append("global_property_account_expense_categ")
        if vals.get("global_property_account_income_categ"):
            field_names.append("global_property_account_income_categ")

        category.propagate_global_account_properties_recursive(field_names)
        return category

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        field_names = []
        if "global_property_account_expense_categ" in vals.keys():
            field_names.append("global_property_account_expense_categ")
        if "global_property_account_income_categ" in vals.keys():
            field_names.append("global_property_account_income_categ")

        self.propagate_global_account_properties_recursive(field_names)
        return res

    def propagate_global_account_properties_recursive(self, field_names):
        ResCompany = self.env["res.company"]

        for field_name in field_names:
            for category in self:
                companies = ResCompany.with_context(active_test=False).search(
                    [("fiscal_type", "in", ["normal", "fiscal_mother", "fiscal_child"])]
                )
                for company in companies:
                    category._apply_global_account_property(company, field_name)

                childs = category.mapped("child_id")
                childs.write({field_name: getattr(category, field_name)})

    @api.multi
    def _apply_global_account_property(self, company, field_name):
        self.ensure_one()
        IrProperty = self.env["ir.property"].sudo()
        AccountAccount = self.env["account.account"].sudo()
        IrModelFields = self.env["ir.model.fields"]

        base_message = "Company {} - Category {}".format(
            company.name, self.complete_name
        )

        account_code = getattr(self, field_name)

        if account_code:
            account = AccountAccount.search(
                [
                    ("code", "=", account_code),
                    ("company_id", "=", company.fiscal_company_id.id),
                ]
            )
            if not account:
                raise UserError(
                    _("{} - Account {} not found.".format(base_message, account_code))
                )

        field = IrModelFields.search(
            [
                ("name", "=", "%s_id" % field_name.replace("global_", "")),
                ("model", "=", "product.category"),
            ]
        )

        current_property = IrProperty.search(
            [
                ("name", "=", field.name),
                ("fields_id", "=", field.id),
                ("company_id", "=", company.id),
                ("res_id", "=", "product.category,%d" % (self.id)),
            ]
        )

        if account_code:
            if current_property:
                # Update Existing Property
                current_property.write(
                    {"value_reference": "account.account,%d" % (account.id)}
                )
                _logger.debug(
                    "{} - Account {} : Property updated.".format(
                        base_message, account_code
                    )
                )
            else:
                # Create a new property
                IrProperty.create(
                    {
                        "name": field.name,
                        "company_id": company.id,
                        "type": "many2one",
                        "fields_id": field.id,
                        "value_reference": "account.account,%d" % (account.id),
                        "res_id": "product.category,%d" % (self.id),
                    }
                )
                _logger.debug(
                    "{} - Account {} : Property created.".format(
                        base_message, account_code
                    )
                )

        elif current_property:
            # Delete obsolete property
            current_property.unlink()
            _logger.debug("%s : Property deleted." % (base_message))
