# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase

from odoo.addons.base_fiscal_company.fix_test import fix_required_field


class TestWizard(TransactionCase):
    """Tests for Account Fiscal Company Module (Wizard)"""

    # Overload Section
    def setUp(self):
        super(TestWizard, self).setUp()
        self.pricelist_obj = self.env['product.pricelist']
        self.wizard_obj = self.env['res.company.create.wizard']
        self.mother_company = self.env.ref(
            'base_fiscal_company.company_fiscal_mother')
        self.user_accountant = self.env.ref(
            'base_fiscal_company.user_accountant')
        fix_required_field(self, 'DROP')

    def tearDown(self):
        self.cr.rollback()
        fix_required_field(self, 'SET')
        super(TestWizard, self).tearDown()

    # Test Section
    def test_01_pricelist_creation(self):
        """[Functional Test] creating a new company via wizard
        should work"""
        wizard = self.wizard_obj.sudo(self.user_accountant).create({
            'company_name': 'Test Company Wizard',
            'fiscal_type': 'fiscal_child',
            'fiscal_code': 'WIZ',
            'parent_company_id': self.mother_company.id,
        })
        wizard.button_begin()
