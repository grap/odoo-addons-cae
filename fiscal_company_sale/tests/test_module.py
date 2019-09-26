# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestModule(TransactionCase):
    """Tests for 'CAE - Sale' Module"""

    # Overload Section
    def setUp(self):
        super().setUp()
        self.SaleOrder = self.env['sale.order']
        self.ResPartner = self.env['res.partner']
        self.user_worker = self.env.ref('fiscal_company_base.user_worker')
        self.child_company = self.env.ref(
            'fiscal_company_base.company_fiscal_child_1')
        self.mother_company = self.env.ref(
            'fiscal_company_base.company_fiscal_mother')

    # Test Section
    def test_01_block_sale_order_creation(self):
        """[Functional Test] Test constraint again sale order creation"""

        # Try to create a sale order in a child company should success
        self._create_sale_order(self.child_company)

        # Try to create a sale order in a mother company should success
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.mother_company)

    def _create_sale_order(self, company):
        partner = self.ResPartner.create({
            'name': 'Test partner',
            'company_id': company.id,
        })
        order_vals = {
            'name': 'Sale Order Test',
            'company_id': company.id,
            'partner_id': partner.id,
        }

        self.user_worker.company_id = company.id
        self.SaleOrder.sudo(self.user_worker).create(order_vals)
