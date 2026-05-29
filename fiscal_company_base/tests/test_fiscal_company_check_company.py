# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .test_abstract import TestAbstract


@tagged("post_install", "-at_install")
class TestFiscalCompanyCheckCompanyMixin(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResPartner = cls.env["res.partner"]

    def test_res_partner_check_fiscal_mother(self):
        self.ResPartner.create({"name": "P1", "company_id": False})
        self.ResPartner.create({"name": "P2", "company_id": self.normal_company.id})
        self.ResPartner.create({"name": "P3", "company_id": self.child_company.id})
        with self.assertRaises(
            ValidationError,
            msg="You can not create a partner with group company",
        ):
            self.ResPartner.create({"name": "P4", "company_id": self.group_company.id})

        with self.assertRaises(
            ValidationError,
            msg="You can not create a partner with fiscal_mother company",
        ):
            self.ResPartner.create({"name": "P5", "company_id": self.mother_company.id})

    def test_res_user_check_fiscal_mother(self):
        self.user_accountant.write({"company_id": self.normal_company.id})
        self.user_accountant.write({"company_id": self.group_company.id})
        self.user_accountant.write({"company_id": self.mother_company.id})
        self.user_accountant.write({"company_id": self.child_company.id})
