# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestAbstract(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResCompany = cls.env["res.company"]
        cls.ResPartner = cls.env["res.partner"]
        cls.group_company = cls.env.ref("fiscal_company_base.company_group")
        cls.mother_company = cls.env.ref("fiscal_company_base.company_fiscal_mother")
        cls.child_company = cls.env.ref("fiscal_company_base.company_fiscal_child_1")
        cls.normal_company = cls.env.ref("base.main_company")
        cls.user_accountant = cls.env.ref("fiscal_company_base.user_accountant")
