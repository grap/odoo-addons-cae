# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestTaxFiltered(TransactionCase):
    """Tests for Account Fiscal Company Module (Tax filter)"""

    def setUp(self):
        super().setUp()
        self.taxes = self.env.ref("fiscal_company_account.sale_tax_20") | self.env.ref(
            "fiscal_company_account.purchase_tax_20"
        )
        self.child_company = self.env.ref("fiscal_company_base.company_fiscal_child_1")
        self.mother_company = self.env.ref("fiscal_company_base.company_fiscal_mother")

    # Test Section
    def test_01_filter_company(self):
        child_company = self.child_company

        for current_company in [self.child_company, self.mother_company]:
            self.env.user.company_id = current_company

            # Check Syntax 1
            filtered_taxes = self.taxes.filtered(
                lambda x: x.company_id == child_company
            )
            self.assertEqual(
                len(filtered_taxes),
                2,
                "Filtering taxes by child company should not filter. (syntax 1)",
            )

            # Check Syntax 2
            filtered_taxes = self.taxes.filtered(
                lambda x: x.company_id.id == child_company.id
            )
            self.assertEqual(
                len(filtered_taxes),
                2,
                "Filtering taxes by child company should not filter. (syntax 2)",
            )

            # Check Syntax 3
            filtered_taxes = self.taxes.filtered(
                lambda x: x.company_id.id == self.child_company.id
            )
            self.assertEqual(
                len(filtered_taxes),
                2,
                "Filtering taxes by child company should not filter. (syntax 2)",
            )

            # Check No Regression (no filter)
            filtered_taxes = self.taxes.filtered(lambda x: "20" in x.name)
            self.assertEqual(
                len(filtered_taxes), 2, "Filtering taxes by name should worker (1/3"
            )

            # Check No Regression (partial filter)
            filtered_taxes = self.taxes.filtered(lambda x: "Purchase" in x.name)
            self.assertEqual(
                len(filtered_taxes), 1, "Filtering taxes by name should worker (2/3"
            )

            # Check No Regression (filter)
            filtered_taxes = self.taxes.filtered(lambda x: "99" in x.name)
            self.assertEqual(
                len(filtered_taxes), 0, "Filtering taxes by name should worker (3/3"
            )

    def test_that_should_fail(self):
        # we test multiple filter in the same time.
        # The non company condition will not be applyed (and should be).
        # It is a limitation of the current implementation.
        # See details in DEVELOP.rst file.
        self.env.user.company_id = self.mother_company
        # the result should be 1, but it will return 2

        filtered_taxes = self.taxes.filtered(
            lambda x: x.company_id.id == self.child_company.id and "Purchase" in x.name
        )
        self.assertEqual(len(filtered_taxes), 2)
