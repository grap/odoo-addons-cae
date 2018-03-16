# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestDecorator(TransactionCase):
    """Tests for Account Fiscal Company Module (Decorator)"""

    def setUp(self):
        super(TestDecorator, self).setUp()
#        self.company_obj = self.env['res.company']
#        self.partner_obj = self.env['res.partner']
#        self.category_obj = self.env['product.category']
#        self.template_obj = self.env['product.template']
#        self.product_obj = self.env['product.product']

#        self.mother_company = self.env.ref(
#            'base_fiscal_company.company_fiscal_mother')
#        self.child_company = self.env.ref(
#            'base_fiscal_company.company_fiscal_child_1')
#        self.account_expense_cae = self.env.ref(
#            'account_fiscal_company.account_expense_cae')
#        self.account_income_cae = self.env.ref(
#            'account_fiscal_company.account_income_cae')
#        self.account_payable_cae = self.env.ref(
#            'account_fiscal_company.account_payable_cae')
#        self.account_receivable_cae = self.env.ref(
#            'account_fiscal_company.account_receivable_cae')
#        self.account_custom_payable_cae = self.env.ref(
#            'account_fiscal_company.account_custom_payable_cae')
#        self.account_custom_receivable_cae = self.env.ref(
#            'account_fiscal_company.account_custom_receivable_cae')

#        # Object with demo accounting properties
#        self.product_category_all = self.env.ref(
#            'product.product_category_all')
#        self.product_template_mother_property = self.env.ref(
#            'account_fiscal_company.product_template_mother_property')
#        self.product_product_mother_property = self.env.ref(
#            'account_fiscal_company.product_product_mother_property')
#        self.partner_mother_property = self.env.ref(
#            'account_fiscal_company.partner_mother_property')

#        # Object without demo accounting properties
#        self.product_category_internal = self.env.ref(
#            'product.product_category_2')
#        self.product_template_mother = self.env.ref(
#            'product_fiscal_company.product_template_mother')
#        self.product_template_child = self.env.ref(
#            'product_fiscal_company.product_template_child')
#        self.product_product_mother = self.env.ref(
#            'product_fiscal_company.product_product_mother')
#        self.product_product_child = self.env.ref(
#            'product_fiscal_company.product_product_child')

    # Test Section
    def test_01_account_journal_decorator(self):
        """A user in a child company should access to the journal of the
        fiscal mother, even if the domain """
        pass

#        self.assertEqual(
#            category.property_account_expense_categ_id.id,
#            self.account_expense_cae.id,
#            "Create a new child company must set expense account property"
#            " of the mother company to the new child company for category.")
