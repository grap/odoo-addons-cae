# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .test_abstract import TestAbstract


@tagged("post_install", "-at_install")
class TestFiscalTypeConstrains(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ResCompany = cls.env["res.company"]
        cls.group_company = cls.env.ref("fiscal_company_base.company_group")
        cls.mother_company = cls.env.ref("fiscal_company_base.company_fiscal_mother")
        cls.child_company = cls.env.ref("fiscal_company_base.company_fiscal_child_1")
        cls.normal_company = cls.env.ref("base.main_company")

    # Test Section
    def test_01_res_company_check_contraint_child_company_normal(self):
        """A 'normal' company can only have parent type == 'group'
        (or no parent)"""
        self.ResCompany.create(
            {
                "name": "new_company_01_A",
                "fiscal_type": "normal",
            }
        )

        self.ResCompany.create(
            {
                "name": "new_company_01_B",
                "fiscal_type": "normal",
                "parent_id": self.group_company.id,
            }
        )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('normal')"
            " and parent company ('normal')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_01_C",
                    "fiscal_type": "normal",
                    "parent_id": self.normal_company.id,
                }
            )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('normal')"
            " and parent company ('fiscal_mother')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_01_D",
                    "fiscal_type": "normal",
                    "parent_id": self.mother_company.id,
                }
            )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('normal')"
            " and parent company ('fiscal_child')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_01_E",
                    "fiscal_type": "normal",
                    "parent_id": self.child_company.id,
                }
            )

    def test_02_res_company_check_contraint_child_company_group(self):
        """A 'group' company can only have parent type == 'group'
        (or no parent)"""
        self.ResCompany.create(
            {
                "name": "new_company_02_A",
                "fiscal_type": "group",
            }
        )

        self.ResCompany.create(
            {
                "name": "new_company_02_B",
                "fiscal_type": "group",
                "parent_id": self.group_company.id,
            }
        )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('group')"
            " and parent company ('normal')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_02_C",
                    "fiscal_type": "group",
                    "parent_id": self.normal_company.id,
                }
            )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('group')"
            " and parent company ('fiscal_mother')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_02_D",
                    "fiscal_type": "group",
                    "parent_id": self.mother_company.id,
                }
            )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('group')"
            " and parent company ('fiscal_child')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_02_E",
                    "fiscal_type": "group",
                    "parent_id": self.child_company.id,
                }
            )

    def test_03_res_company_check_contraint_child_company_fiscal_mother(self):
        """A 'fiscal_mother' company can only have parent type == 'group'
        (or no parent)"""
        self.ResCompany.create(
            {
                "name": "new_company_03_A",
                "fiscal_type": "fiscal_mother",
            }
        )

        self.ResCompany.create(
            {
                "name": "new_company_03_B",
                "fiscal_type": "fiscal_mother",
                "parent_id": self.group_company.id,
            }
        )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('fiscal_mother')"
            " and parent company ('normal')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_03_C",
                    "fiscal_type": "fiscal_mother",
                    "parent_id": self.normal_company.id,
                }
            )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('fiscal_mother')"
            " and parent company ('fiscal_mother')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_03_D",
                    "fiscal_type": "fiscal_mother",
                    "parent_id": self.mother_company.id,
                }
            )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('fiscal_mother')"
            " and parent company ('fiscal_child')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_03_E",
                    "fiscal_type": "fiscal_mother",
                    "parent_id": self.child_company.id,
                }
            )

    def test_04_res_company_check_contraint_child_company_fiscal_child(self):
        """A 'fiscal_child' company can only have parent type == 'fiscal_mother'"""
        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('fiscal_child')"
            " without parent company",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_04_A",
                    "fiscal_type": "fiscal_child",
                }
            )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('fiscal_child')"
            " and parent company ('group')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_04_B",
                    "fiscal_type": "fiscal_child",
                    "parent_id": self.group_company.id,
                }
            )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('fiscal_child')"
            " and parent company ('normal')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_04_C",
                    "fiscal_type": "fiscal_child",
                    "parent_id": self.normal_company.id,
                }
            )

        self.ResCompany.create(
            {
                "name": "new_company_04_D",
                "fiscal_type": "fiscal_child",
                "parent_id": self.mother_company.id,
            }
        )

        with self.assertRaises(
            ValidationError,
            msg="You can not create a child company ('fiscal_child')"
            " and parent company ('fiscal_child')",
        ):
            self.ResCompany.create(
                {
                    "name": "new_company_04_E",
                    "fiscal_type": "fiscal_child",
                    "parent_id": self.child_company.id,
                }
            )

    def test_10_res_company_check_contraint_parent_company_set_normal(self):
        with self.assertRaises(
            ValidationError,
            msg="You can not set as 'normal' company"
            " a company that contains other companies.",
        ):
            self.group_company.fiscal_type = "normal"

        with self.assertRaises(
            ValidationError,
            msg="You can not set as 'normal' company"
            " a company that contains other companies.",
        ):
            self.mother_company.fiscal_type = "normal"

    def test_11_res_company_check_contraint_parent_company_set_fiscal_mother(self):
        with self.assertRaises(
            ValidationError,
            msg="You can not set as 'fiscal_mother' company"
            " a company that doesn't contains only fiscal_child companies.",
        ):
            self.group_company.fiscal_type = "fiscal_mother"

    def test_12_res_company_check_contraint_parent_company_set_fiscal_child(self):
        with self.assertRaises(
            ValidationError,
            msg="You can not set as 'fiscal_child' company"
            " a company that contains other companies.",
        ):
            self.group_company.fiscal_type = "fiscal_child"

        with self.assertRaises(
            ValidationError,
            msg="You can not set as 'fiscal_child' company"
            " a company that contains other companies.",
        ):
            self.mother_company.fiscal_type = "fiscal_child"

    def test_13_res_company_check_contraint_parent_company_set_group(self):
        with self.assertRaises(
            ValidationError,
            msg="You can not set as 'group' company"
            " a company that contains fiscal_child companies.",
        ):
            self.mother_company.fiscal_type = "group"
