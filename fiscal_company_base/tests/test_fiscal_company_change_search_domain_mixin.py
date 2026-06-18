# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from .test_abstract import TestAbstract


class TestFiscalCompanyChangeSearchDomainMixin(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load a test model using odoo_test_helper
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ModelFiscalCompanyChangeSearchDomainMixin

        cls.loader.update_registry((ModelFiscalCompanyChangeSearchDomainMixin,))

        cls.model = cls.env["model.fiscal.company.change.search.domain.mixin"]
        cls.model.create(
            [
                {"company_id": False},
                {"company_id": cls.group_company.id},
                {"company_id": cls.normal_company.id},
                {"company_id": cls.mother_company.id},
                {"company_id": cls.child_company.id},
            ]
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def _check_domain(self, domain, expected_new_domain):
        new_domain = self.model._fiscal_company_change_domain(domain)
        self.assertEqual(new_domain, expected_new_domain)

    def test_01_search(self):
        self.assertEqual(
            len(self.model.search([("company_id", "=", False)])),
            1,
        )
        self.assertEqual(
            len(self.model.search([("company_id", "=", self.group_company.id)])),
            1,
        )
        self.assertEqual(
            len(self.model.search([("company_id", "=", self.normal_company.id)])),
            1,
        )
        self.assertEqual(
            len(self.model.search([("company_id", "=", self.mother_company.id)])),
            1,
        )
        self.assertEqual(
            len(self.model.search([("company_id", "=", self.child_company.id)])),
            2,
        )

    def test_10_fiscal_company_change_domain_no_changes(self):
        self._check_domain(
            [("company_id", "=", False)],
            [("company_id", "=", False)],
        )
        self._check_domain(
            [("company_id", "=", self.group_company.id)],
            [("company_id", "=", self.group_company.id)],
        )
        self._check_domain(
            [("company_id", "=", self.normal_company.id)],
            [("company_id", "=", self.normal_company.id)],
        )
        self._check_domain(
            [("company_id", "=", self.mother_company.id)],
            [("company_id", "=", self.mother_company.id)],
        )

    def test_11_fiscal_company_change_domain_with_changes(self):
        self._check_domain(
            [("company_id", "=", self.child_company.id)],
            [("company_id", "in", [self.child_company.id, self.mother_company.id])],
        )

        self._check_domain(
            [("company_id", "in", [self.child_company.id, False])],
            [
                (
                    "company_id",
                    "in",
                    [self.child_company.id, self.mother_company.id, False],
                )
            ],
        )
