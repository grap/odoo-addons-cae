# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.fiscal_company_base.tests import test_abstract


class TestAbstract(test_abstract.TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AccountAccount = cls.env["account.account"]
        cls.ProductProduct = cls.env["product.product"]
        cls.AccountMove = cls.env["account.move"]
        cls.AccountJournal = cls.env["account.journal"]
