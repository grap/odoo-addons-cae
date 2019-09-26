# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase

# from odoo.addons.fiscal_company_base.fix_test import fix_required_field


class TestPropagateProperties(TransactionCase):
    """Tests for Account Fiscal Company Module (Propagate Properties)"""

    def setUp(self):
        super().setUp()
        self.ResCompany = self.env['res.company']
        self.ResPartner = self.env['res.partner']
        self.ProductCategory = self.env['product.category']
        self.ProductTemplate = self.env['product.template']
        self.ProductProduct = self.env['product.product']

        self.mother_company = self.env.ref(
            'fiscal_company_base.company_fiscal_mother')
        self.child_company = self.env.ref(
            'fiscal_company_base.company_fiscal_child_1')
        self.account_expense_cae = self.env.ref(
            'fiscal_company_account.account_expense_cae')
        self.account_income_cae = self.env.ref(
            'fiscal_company_account.account_income_cae')
        self.account_payable_cae = self.env.ref(
            'fiscal_company_account.account_payable_cae')
        self.account_receivable_cae = self.env.ref(
            'fiscal_company_account.account_receivable_cae')
        self.account_custom_payable_cae = self.env.ref(
            'fiscal_company_account.account_custom_payable_cae')
        self.account_custom_receivable_cae = self.env.ref(
            'fiscal_company_account.account_custom_receivable_cae')

        self.accountant = self.env.ref('fiscal_company_base.user_accountant')

        # Object with demo accounting properties
        self.product_category_all = self.env.ref(
            'product.product_category_all')
        self.product_template_mother_property = self.env.ref(
            'fiscal_company_account.product_template_mother_property')
        self.product_product_mother_property = self.env.ref(
            'fiscal_company_account.product_product_mother_property')
        self.partner_mother_property = self.env.ref(
            'fiscal_company_account.partner_mother_property')

        # Object without demo accounting properties
        self.product_category_internal = self.env.ref(
            'product.product_category_2')
        self.product_template_mother = self.env.ref(
            'fiscal_company_product.product_template_mother')
        self.product_template_child = self.env.ref(
            'fiscal_company_product.product_template_child')
        self.product_product_mother = self.env.ref(
            'fiscal_company_product.product_product_mother')
        self.product_product_child = self.env.ref(
            'fiscal_company_product.product_product_child')
        # fix_required_field(self, 'DROP')

    # def tearDown(self):
    #     self.cr.rollback()
    #     fix_required_field(self, 'SET')
    #     super().tearDown()

    # Test Section
    def test_01_account_property_propagation_new_company(self):
        """Create a new child company must propagate categories properties"""

        # Create a new Child company
        child_company = self.ResCompany.create({
            'name': 'Your Test Child Company',
            'fiscal_type': 'fiscal_child',
            'fiscal_company_id': self.mother_company.id,
            'parent_id': self.mother_company.id,
        })

        # Change current company and load objects with the new context
        self.env.user.company_id = child_company.id

        # Check if category properties has been propagated for the new company
        category = self.ProductCategory.browse(
            [self.product_category_all.id])
        self.assertEqual(
            category.property_account_expense_categ_id.id,
            self.account_expense_cae.id,
            "Create a new child company must set expense account property"
            " of the mother company to the new child company for category.")

        self.assertEqual(
            category.property_account_income_categ_id.id,
            self.account_income_cae.id,
            "Create a new child company must set income account property"
            " of the mother company to the new child company for category.")

        # Check if product properties has been propagated for the new company
        product = self.ProductProduct.browse(
            [self.product_product_mother_property.id])
        self.assertEqual(
            product.property_account_expense_id.id,
            self.account_expense_cae.id,
            "Create a new child company must set expense account property"
            " of the mother company to the new child company for product.")

        self.assertEqual(
            product.property_account_income_id.id,
            self.account_income_cae.id,
            "Create a new child company must set income account property"
            " of the mother company to the new child company for product.")

        # Check if template properties has been propagated for the new company
        template = self.ProductTemplate.browse(
            [self.product_template_mother_property.id])
        self.assertEqual(
            template.property_account_expense_id.id,
            self.account_expense_cae.id,
            "Create a new child company must set expense account property"
            " of the mother company to the new child company for template.")

        self.assertEqual(
            template.property_account_income_id.id,
            self.account_income_cae.id,
            "Create a new child company must set income account property"
            " of the mother company to the new child company for template.")

        # Check if custom partner properties has been propagated for the new
        # company
        partner = self.ResPartner.browse(
            [self.partner_mother_property.id])
        self.assertEqual(
            partner.property_account_payable_id.id,
            self.account_custom_payable_cae.id,
            "Create a new child company must set custom payable account"
            " property of the mother company to the new child company for"
            " partner.")

        self.assertEqual(
            partner.property_account_receivable_id.id,
            self.account_custom_receivable_cae.id,
            "Create a new child company must set custom receivable account"
            " property of the mother company to the new child company for"
            " partner.")

    def test_02_category_propagate_fiscal_property_to_all(self):
        """Change a category property of a fiscal company must change the value
        for all other companies"""

        # Change current company
        self.env.user.company_id = self.mother_company.id

        self.product_category_internal.write({
            'property_account_expense_categ_id': self.account_expense_cae.id,
            'property_account_income_categ_id': self.account_income_cae.id,
        })

        # Change current company and load category with the new context
        self.env.user.company_id = self.child_company.id
        category = self.ProductCategory.browse(
            [self.product_category_internal.id])

        # Check if properties has been propagated to the other company
        self.assertEqual(
            category.property_account_expense_categ_id.id,
            self.account_expense_cae.id,
            "Change an expense property for a category in a fiscal company"
            " must change the value for all the other fiscal company.")

        self.assertEqual(
            category.property_account_income_categ_id.id,
            self.account_income_cae.id,
            "Change an income property for a category in a fiscal company"
            " must change the value for all the other fiscal company.")

    def test_03_template_mother_propagate_fiscal_property_to_all(self):
        """Change a template property of a fiscal company must change the value
        for all other companies if the template belong to the
        fiscal mother company"""

        template_id = self.env.ref(
            'fiscal_company_product.product_template_mother').id

        ProductTemplateAccountant = self.env['product.template'].sudo(
            self.accountant)
        self.accountant.company_id = self.mother_company.id

        templateInMotherCompany = ProductTemplateAccountant.browse(template_id)

        templateInMotherCompany.write({
            'property_account_expense_id': self.account_expense_cae.id,
            'property_account_income_id': self.account_income_cae.id,
        })

        # Change current company and load template with the new context
        self.accountant.company_id = self.child_company.id

        # self.env.user.company_id = self.child_company.id
        templateInChildCompany = ProductTemplateAccountant.browse(template_id)

        # Check if properties has been propagated to the other company
        self.assertEqual(
            templateInChildCompany.property_account_expense_id.id,
            self.account_expense_cae.id,
            "Change an expense property for a template in a mother company"
            " must change the value for all the other fiscal company.")

        self.assertEqual(
            templateInChildCompany.property_account_income_id.id,
            self.account_income_cae.id,
            "Change an income property for a template in a mother company"
            " must change the value for all the other fiscal company.")

    def test_04_template_child_propagate_fiscal_property_to_all(self):
        """Change a template property of a fiscal company must not change the
         value for all other companies if the template belong to a
        fiscal child company"""

        # Change current company
        self.env.user.company_id = self.child_company.id

        self.product_template_child.write({
            'property_account_expense_id': self.account_expense_cae.id,
            'property_account_income_id': self.account_income_cae.id,
        })

        # Change current company and load template with the new context
        self.env.user.company_id = self.mother_company.id
        template = self.ProductTemplate.browse(
            [self.product_template_child.id])

        # Check if properties has not been propagated to the other company
        self.assertNotEqual(
            template.property_account_expense_id.id,
            self.account_expense_cae.id,
            "Change an expense property for a template in a child company"
            " must change the value for all the other fiscal company.")

        self.assertNotEqual(
            template.property_account_income_id.id,
            self.account_income_cae.id,
            "Change an income property for a template in a child company"
            " must not change the value for all the other fiscal company.")

    def test_05_product_mother_propagate_fiscal_property_to_all(self):
        """Change a product property of a fiscal company must change the value
        for all other companies if the product belong to the
        fiscal mother company"""

        product_id = self.env.ref(
            'fiscal_company_account.product_product_mother_property').id

        ProductProductAccountant = self.env['product.product'].sudo(
            self.accountant)

        # Change current company
        self.accountant.company_id = self.mother_company.id

        productInMotherCompany = ProductProductAccountant.browse(product_id)

        productInMotherCompany.write({
            'property_account_expense_id': self.account_expense_cae.id,
            'property_account_income_id': self.account_income_cae.id,
        })

        # Change current company and load template with the new context
        self.accountant.company_id = self.child_company.id

        # self.env.user.company_id = self.child_company.id
        productInChildCompany = ProductProductAccountant.browse(product_id)

        # Check if properties has been propagated to the other company
        self.assertEqual(
            productInChildCompany.property_account_expense_id.id,
            self.account_expense_cae.id,
            "Change an expense property for a product in a mother company"
            " must change the value for all the other fiscal company.")

        self.assertEqual(
            productInChildCompany.property_account_income_id.id,
            self.account_income_cae.id,
            "Change an income property for a product in a mother company"
            " must change the value for all the other fiscal company.")

    def test_06_product_child_propagate_fiscal_property_to_all(self):
        """Change a product property of a fiscal company must not change the
         value for all other companies if the product belong to a
        fiscal child company"""

        # Change current company
        self.env.user.company_id = self.child_company.id

        self.product_product_child.write({
            'property_account_expense_id': self.account_expense_cae.id,
            'property_account_income_id': self.account_income_cae.id,
        })

        # Change current company and load product with the new context
        self.env.user.company_id = self.mother_company.id
        product = self.ProductProduct.browse([self.product_product_child.id])

        # Check if properties has not been propagated to the other company
        self.assertNotEqual(
            product.property_account_expense_id.id,
            self.account_expense_cae.id,
            "Change an expense property for a product in a child company"
            " must change the value for all the other fiscal company.")

        self.assertNotEqual(
            product.property_account_income_id.id,
            self.account_income_cae.id,
            "Change an income property for a product in a child company"
            " must not change the value for all the other fiscal company.")
