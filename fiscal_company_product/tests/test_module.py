# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    """Tests for 'CAE - Product' Module"""

    # Overload Section
    def setUp(self):
        super().setUp()
        self.ProductProduct = self.env["product.product"]
        self.user_accountant = self.env.ref("fiscal_company_base.user_accountant")
        self.user_worker = self.env.ref("fiscal_company_base.user_worker")
        self.child_company = self.env.ref("fiscal_company_base.company_fiscal_child_1")
        self.product_categ = self.env.ref("product.product_category_1")

        # Dirty Hack:
        # Accountant can create a product, but can't create a product.history.
        # (ugly Odoo ORM !)
        # So, we set a correct setting for that model for our tests.
        self.access = self.env.ref("product.access_product_price_history_employee")
        self.access.perm_create = True

    # Test Section
    def test_01_administrative_product_creation(self):
        """[Functional Test] Test constraint again Administrative product"""

        # Try to create an administrative product with user that is
        # CAE manager, should success
        product = self._create_administrative_product(self.user_accountant)

        # Try to create an administrative product with user that is not
        # CAE manager, should fail
        with self.assertRaises(ValidationError):
            self._create_administrative_product(self.user_worker)

        # Try to write on administrative product with user that is not
        # CAE manager should fail if the field is protected
        with self.assertRaises(ValidationError):
            product.sudo(self.user_worker).write({"name": "New name"})

        # Try to write on administrative product with user that is not
        # CAE manager should success if the field is not protected
        with self.assertRaises(ValidationError):
            product.sudo(self.user_worker).write({"lst_price": 5.0})

    def _create_administrative_product(self, user):
        product_vals = {
            "name": "Product Test",
            "company_id": self.child_company.id,
            "categ_id": self.product_categ.id,
            "cae_administrative_ok": True,
        }
        user.company_id = self.child_company.id
        return (
            self.ProductProduct.sudo(user)
            .with_context(mail_create_nosubscribe=True, mail_create_nolog=True)
            .create(product_vals)
        )
