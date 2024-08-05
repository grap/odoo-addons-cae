# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from .test_abstract import TestAbstract


class TestWithCompany(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load a test model using odoo_test_helper
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ModelWithCompany

        cls.loader.update_registry((ModelWithCompany,))

        cls.model_with_company = cls.env["model.with.company"]

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_with_company_change_disabled(self):
        res = self.model_with_company.with_company_disabled(self.mother_company)
        self.assertEqual(res.env.company, self.normal_company)

    def test_with_company_change_enabled(self):
        res = self.model_with_company.with_company_enabled(self.mother_company)
        self.assertEqual(res.env.company, self.mother_company)
