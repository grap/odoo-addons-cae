# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from .test_abstract import TestAbstract


class TestFiscalCompanyPropagateChildCompanyMixin(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load a test model using odoo_test_helper
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import (
            ModelFiscalCompanyPropagateChildCompanyMixin,
            ModelFiscalCompanyPropagateChildCompanyMixinResCompany,
        )

        cls.loader.update_registry(
            (
                ModelFiscalCompanyPropagateChildCompanyMixin,
                ModelFiscalCompanyPropagateChildCompanyMixinResCompany,
            )
        )

        cls.model_propagate_child_company = cls.env[
            "model.fiscal.company.propagate.child.company.mixin"
        ]

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_check_propagation_ok(self):
        item = self.model_propagate_child_company.with_company(
            self.mother_company
        ).create({"company_dependent_field": "BOB"})
        new_child_company = self.env["res.company"].create(
            {
                "name": "NEW FISCAL CHILD",
                "parent_id": self.mother_company.id,
                "fiscal_type": "fiscal_child",
            }
        )
        self.assertEqual(
            item.with_company(new_child_company).company_dependent_field, "BOB"
        )
        self.assertEqual(
            item.with_company(self.normal_company).company_dependent_field, False
        )
