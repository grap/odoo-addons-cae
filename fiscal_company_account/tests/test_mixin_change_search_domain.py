# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from .test_abstract import TestAbstract


class TestMixinChangeSearchDomain(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_accountant.company_id = cls.child_company.id

    # Test Section
    def test_01_mixin_change_search_domain_account_account(self):
        """Searching an account in a child company should return
        accounts of the mother company"""
        res = self.AccountAccount.with_user(self.user_accountant).search(
            [("company_id", "=", self.mother_company.id)]
        )
        self.assertNotEqual(
            len(res),
            0,
            "Searching accounts in a fiscal child company should return"
            " accounts of the mother company",
        )

    def test_02_mixin_change_search_domain_account_journal(self):
        """Searching a journal in a child company should return
        journals of the mother company"""
        self.user_accountant.company_id = self.child_company.id
        res = self.AccountJournal.with_user(self.user_accountant).search(
            [("company_id", "=", self.mother_company.id)]
        )
        self.assertNotEqual(
            len(res),
            0,
            "Searching accounts in a fiscal child company should return"
            " accounts of the mother company",
        )
