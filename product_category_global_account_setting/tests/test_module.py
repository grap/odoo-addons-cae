# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResCompany = cls.env["res.company"]
        cls.AccountAccount = cls.env["account.account"]
        cls.IrProperty = cls.env["ir.property"].sudo()
        cls.mother_company = cls.env.ref("fiscal_company_base.company_fiscal_mother")
        cls.saleable_categ = cls.env.ref("product.product_category_1")
        cls.saleable_service_categ = cls.env.ref("product.product_category_3")
        cls.expense_field = cls.env.ref(
            "account." "field_product_category__property_account_expense_categ_id"
        )

    def _create_account_for_all_companies(self, code, name, account_type):
        for company in self.ResCompany.with_context(active_test=False).search(
            [("fiscal_type", "in", ["normal", "fiscal_mother"])]
        ):
            self.AccountAccount.sudo().create(
                {
                    "code": code,
                    "name": name,
                    "account_type": account_type,
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
        self._create_account_for_all_companies("607TEST", "Purchase", "expense")
        self.saleable_categ.write({"global_property_account_expense_categ": "607TEST"})

        self._create_account_for_all_companies("707TEST", "Sale", "income")
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
        self._create_account_for_all_companies("607TEST", "Purchase", "expense")

        self.saleable_categ.write({"global_property_account_expense_categ": "607TEST"})

        # Try to create a fiscal child should create new properties
        new_company = self.ResCompany.create(
            {
                "name": "Test Fiscal Child Company (Global Account)",
                "fiscal_type": "fiscal_child",
                "parent_id": self.mother_company.id,
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
