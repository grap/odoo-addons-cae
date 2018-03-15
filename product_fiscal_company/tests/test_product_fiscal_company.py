# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductFiscalCompany(TransactionCase):
    """Tests for 'Product Fiscal Company' Module"""

    # Overload Section
    def setUp(self):
        super(TestProductFiscalCompany, self).setUp()
        self.pricelist_obj = self.env['product.pricelist']
        self.wizard_obj = self.env['res.company.create.wizard']
        self.mother_company = self.env.ref(
            'base_fiscal_company.company_fiscal_mother')

    # Test Section
    def test_01_pricelist_creation(self):
        """[Functional Test] creating a new company via wizard should create
        a pricelist"""
        wizard = self.wizard_obj.create({
            'company_name': 'Test Company Wizard',
            'fiscal_type': 'fiscal_child',
            'fiscal_code': 'WIZ',
            'parent_company_id': self.mother_company.id,
        })
        wizard.button_begin()
        wizard.button_finish()
        pricelists = self.pricelist_obj.search([
            ('company_id', '=', wizard.company_id.id),
            ('name', '=', 'WIZ - Public Pricelist'),
        ])
        self.assertEqual(
            len(pricelists), 1,
            "Create a company by wizard should create a pricelist")
