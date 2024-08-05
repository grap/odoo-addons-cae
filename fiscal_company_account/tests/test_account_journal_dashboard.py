# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json

from odoo import Command

from .test_abstract import TestAbstract


class TestAccountJournalDashboard(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_accountant.company_id = cls.child_company

        move_vals = {
            "partner_id": cls.ResPartner.with_user(cls.user_accountant)
            .search([])[0]
            .id,
            "move_type": "out_invoice",
            "line_ids": [
                Command.create(
                    {
                        "product_id": cls.ProductProduct.with_user(cls.user_accountant)
                        .search([])[0]
                        .id
                    }
                )
            ],
        }
        cls.move1 = cls.AccountMove.with_user(cls.user_accountant).create(move_vals)
        cls.move2 = cls.AccountMove.with_user(cls.user_accountant).create(move_vals)
        cls.move3 = cls.AccountMove.with_user(cls.user_accountant).create(move_vals)
        (cls.move1 | cls.move2).action_post()

    def test_01_dashboard_in_fiscal_child(self):
        self.user_accountant.company_id = self.child_company
        sale_journal = self.AccountJournal.with_user(self.user_accountant).search(
            [("type", "=", "sale")]
        )
        res = json.loads(sale_journal.kanban_dashboard)
        self.assertEqual(res.get("number_draft"), 1)
        self.assertEqual(res.get("number_waiting"), 2)
        self.assertEqual(res.get("entries_count"), 3)

        res = json.loads(sale_journal.kanban_dashboard_graph)
        self.assertEqual(len(res[0].get("values")), 0)

    def test_02_dashboard_in_fiscal_mother(self):
        self.user_accountant.company_id = self.mother_company
        sale_journal = self.AccountJournal.with_user(self.user_accountant).search(
            [("type", "=", "sale")]
        )
        res = json.loads(sale_journal.kanban_dashboard)
        self.assertEqual(res.get("number_draft"), 0)
        self.assertEqual(res.get("number_waiting"), 0)
        self.assertEqual(res.get("entries_count"), 0)

        res = json.loads(sale_journal.kanban_dashboard_graph)
        self.assertEqual(len(res[0].get("values")), 6)
