# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.fiscal_company_base.tests.test_abstract import TestAbstract


class TestFiscalCompanyPropagatedFields(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.correct_siren = "123456782"

    def test_propagated_fields_group(self):
        self.group_company.siren = self.correct_siren
        self.assertEqual(self.mother_company.siren, False)
        self.assertEqual(self.child_company.siren, False)

    def test_propagated_fields_fiscal_mother(self):
        self.mother_company.siren = self.correct_siren
        self.assertEqual(self.group_company.siren, False)
        self.assertEqual(self.mother_company.siren, self.correct_siren)
        self.assertEqual(self.child_company.siren, self.correct_siren)
