# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    """Tests for 'CAE - Sale' Module"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.SaleOrder = cls.env["sale.order"]
        cls.user_worker = cls.env.ref("fiscal_company_base.user_worker")
        cls.child_company = cls.env.ref("fiscal_company_base.company_fiscal_child_1")
        cls.mother_company = cls.env.ref("fiscal_company_base.company_fiscal_mother")
        cls.global_partner = cls.env["res.partner"].create(
            {"name": "Test partner", "company_id": False}
        )

    # Test Section
    def test_01_block_sale_order_creation(self):
        """[Functional Test] Test constraint again sale order creation"""

        # Try to create a sale order in a child company should success
        self._create_sale_order(self.child_company)

        # Try to create a sale order in a mother company should fail
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.mother_company)

    def _create_sale_order(self, company):
        order_vals = {
            "name": "Sale Order Test",
            "company_id": company.id,
            "partner_id": self.global_partner.id,
        }

        self.user_worker.company_id = company.id
        self.SaleOrder.with_user(self.user_worker).create(order_vals)
