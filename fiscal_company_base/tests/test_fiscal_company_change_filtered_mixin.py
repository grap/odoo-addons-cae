# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from .test_abstract import TestAbstract


class TestFiscalCompanyChangeFilteredMixin(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load a test model using odoo_test_helper
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ModelFiscalCompanyChangeFilteredMixin

        cls.loader.update_registry((ModelFiscalCompanyChangeFilteredMixin,))

        cls.model = cls.env["model.fiscal.company.change.filtered.mixin"]
        cls.items = cls.model.create(
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

    def test_filtered(self):
        result = self.items.filtered(lambda x: True)
        self.assertEqual(len(self.items), 5)

        result = self.items.with_company(self.child_company).filtered(
            lambda x: x.company_id == self.child_company
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result.company_id, self.mother_company)
