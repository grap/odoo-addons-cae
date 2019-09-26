# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase

# from odoo.addons.fiscal_company_base.fix_test import fix_required_field


class TestDecorator(TransactionCase):
    """Tests for Account Fiscal Company Module (Decorator)"""

    def setUp(self):
        super().setUp()
        self.AccountAccount = self.env['account.account']
        self.AccountJournal = self.env['account.journal']
        self.user_accountant = self.env.ref(
            'fiscal_company_base.user_accountant')
        self.child_company = self.env.ref(
            'fiscal_company_base.company_fiscal_child_1')
        self.mother_company = self.env.ref(
            'fiscal_company_base.company_fiscal_mother')
        # fix_required_field(self, 'DROP')

    # def tearDown(self):
    #     self.cr.rollback()
    #     fix_required_field(self, 'SET')
    #     super().tearDown()

    # Test Section
    def test_01_decorator_account_account(self):
        """Searching an account in a child company should return
        accounts of the mother company"""
        self.user_accountant.company_id = self.child_company.id
        res = self.AccountAccount.sudo(self.user_accountant).search(
            [('company_id', '=', self.mother_company.id)])
        self.assertNotEqual(
            len(res), 0,
            "Searching accounts in a fiscal child company should return"
            " accounts of the mother company")

    # Test Section
    def test_02_decorator_account_journal(self):
        """Searching a journal in a child company should return
        journals of the mother company"""
        self.user_accountant.company_id = self.child_company.id
        res = self.AccountJournal.sudo(self.user_accountant).search(
            [('company_id', '=', self.mother_company.id)])
        self.assertNotEqual(
            len(res), 0,
            "Searching accounts in a fiscal child company should return"
            " accounts of the mother company")
