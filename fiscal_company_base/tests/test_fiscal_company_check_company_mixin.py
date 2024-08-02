# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from odoo.exceptions import ValidationError

from .test_abstract import TestAbstract


class TestFiscalCompanyCheckCompanyMixin(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load a test model using odoo_test_helper
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import FiscalCompanyCheckCompanyMixinFiscalMother

        cls.loader.update_registry((FiscalCompanyCheckCompanyMixinFiscalMother,))

        cls.model_fiscal_mother = cls.env[
            "model.fiscal.company.check.company.mixin.fiscal.mother"
        ]

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_check_fiscal_mother(self):
        self.model_fiscal_mother.create({"company_id": False})
        self.model_fiscal_mother.create({"company_id": self.group_company.id})
        self.model_fiscal_mother.create({"company_id": self.normal_company.id})
        with self.assertRaises(
            ValidationError,
            msg="You can not create an item with fiscal_mother"
            " company, due to mixin.",
        ):
            self.model_fiscal_mother.create({"company_id": self.mother_company.id})
        self.model_fiscal_mother.create({"company_id": self.child_company.id})
