# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ResCompany = self.env["res.company"]
        self.AccountAccount = self.env["account.account"]
        self.IrProperty = self.env["ir.property"].sudo()

        self.expense_type = self.env.ref("account.data_account_type_expenses")
        self.mother_company = self.env.ref("fiscal_company_base.company_fiscal_mother")
        self.income_type = self.env.ref("account.data_account_type_revenue")
        self.saleable_categ = self.env.ref("product.product_category_1")
        self.saleable_service_categ = self.env.ref("product.product_category_3")
        self.expense_field = self.env.ref(
            "account." "field_product_category__property_account_expense_categ_id"
        )
        self.income_field = self.env.ref(
            "account." "field_product_category__property_account_income_categ_id"
        )
        self.chart_template = self.env.ref(
            "product_category_global_account_setting.chart_template"
        )
        self.account_template = self.env.ref(
            "product_category_global_account_setting.account_template"
        )

    def _create_account_for_all_companies(self, code, name, user_type_id):
        for company in self.ResCompany.with_context(active_test=False).search(
            [("fiscal_type", "in", ["normal", "fiscal_mother"])]
        ):
            self.AccountAccount.sudo().create(
                {
                    "code": code,
                    "name": name,
                    "user_type_id": user_type_id,
                    "company_id": company.id,
                }
            )

    def test_01_propagate_recursively(self):
        # Try to affect properties should fail
        # if account doesn't exists
        with self.assertRaises(UserError):
            self.saleable_categ.write(
                {"global_property_account_expense_categ": "607TEST"}
            )
        with self.assertRaises(UserError):
            self.saleable_categ.write(
                {"global_property_account_income_categ": "707TEST"}
            )

        # Try to affect properties should success
        # if account exists
        self._create_account_for_all_companies(
            "607TEST", "Purchase", self.expense_type.id
        )
        self.saleable_categ.write({"global_property_account_expense_categ": "607TEST"})

        self._create_account_for_all_companies("707TEST", "Sale", self.income_type.id)
        self.saleable_categ.write({"global_property_account_income_categ": "707TEST"})

        companies = self.ResCompany.with_context(active_test=False).search(
            [("fiscal_type", "in", ["normal", "fiscal_mother", "fiscal_child"])]
        )

        properties = self.IrProperty.search(
            [
                ("fields_id", "=", self.expense_field.id),
                ("company_id", "!=", False),
                ("res_id", "=", "product.category,%d" % (self.saleable_categ.id)),
            ]
        )

        self.assertEqual(
            len(companies),
            len(properties),
            "Affect a global setting to a category should create"
            " a property for each company.",
        )

        # Remove the Global property
        self.saleable_categ.write({"global_property_account_expense_categ": False})

        properties = self.IrProperty.search(
            [
                ("fields_id", "=", self.expense_field.id),
                ("company_id", "!=", False),
                ("res_id", "=", "product.category,%d" % (self.saleable_categ.id)),
            ]
        )

        self.assertEqual(
            0,
            len(properties),
            "Remove a global setting to a category should delete"
            " properties for all companies.",
        )

    def test_02_fiscal_child_company(self):
        self._create_account_for_all_companies(
            "607TEST", "Purchase", self.expense_type.id
        )

        self.saleable_categ.write({"global_property_account_expense_categ": "607TEST"})

        # Try to create a fiscal child should create new properties
        new_company = self.ResCompany.create(
            {
                "name": "Test Fiscal Child Company (Global Account)",
                "fiscal_type": "fiscal_child",
                "fiscal_company_id": self.mother_company.id,
            }
        )

        properties = self.IrProperty.search(
            [
                ("fields_id", "=", self.expense_field.id),
                ("company_id", "=", new_company.id),
                ("res_id", "=", "product.category,%d" % (self.saleable_categ.id)),
            ]
        )

        self.assertEqual(
            1, len(properties), "Create a new fiscal company should create properties"
        )

    def test_03_fiscal_mother_company(self):
        self._create_account_for_all_companies(
            "607TEST", "Purchase", self.expense_type.id
        )

        self.saleable_categ.write({"global_property_account_expense_categ": "607TEST"})

        # Create a fiscal mother
        new_company = self.ResCompany.create(
            {
                "name": "Test Fiscal Mother Company (Global Account)",
                "fiscal_type": "fiscal_mother",
            }
        )

        self.env.user.write({"company_id": new_company.id})

        # Try to install a chart of account without 607TEST
        # should fail
        with self.assertRaises(UserError):
            self.chart_template.load_for_current_company(0, 0)

        # Affect the 607TEST account template to the chart template
        # and try to install again chart of account, should success
        self.account_template.chart_template_id = self.chart_template.id
        self.chart_template.load_for_current_company(0, 0)
