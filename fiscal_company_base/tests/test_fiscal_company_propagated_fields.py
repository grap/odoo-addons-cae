# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .test_abstract import TestAbstract


class TestFiscalCompanyPropagatedFields(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.correct_vat = "FR23334175221"

    def test_propagated_fields_group(self):
        self.group_company.vat = self.correct_vat
        self.assertEqual(self.mother_company.vat, False)
        self.assertEqual(self.child_company.vat, False)

    def test_propagated_fields_fiscal_mother(self):
        self.mother_company.vat = self.correct_vat
        self.assertEqual(self.group_company.vat, False)
        self.assertEqual(self.mother_company.vat, self.correct_vat)
        self.assertEqual(self.child_company.vat, self.correct_vat)
