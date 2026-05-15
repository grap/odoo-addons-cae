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

        cls.sale_journal_accountant_context = cls.AccountJournal.with_user(
            cls.user_accountant
        ).browse(cls.sale_journal.id)

        move_vals = {
            "company_id": cls.child_company.id,
            "partner_id": cls.ResPartner.with_user(cls.user_accountant)
            .search([])[0]
            .id,
            "move_type": "out_invoice",
            "journal_id": cls.sale_journal.id,
            "invoice_date": "2019-01-21",
            "invoice_date_due": "2019-01-21",
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
        res = json.loads(self.sale_journal_accountant_context.kanban_dashboard)
        self.assertEqual(res.get("number_draft"), 1, f"Child company context : {res}")
        self.assertEqual(res.get("number_waiting"), 2, f"Child company context : {res}")
        self.assertEqual(res.get("entries_count"), 3, f"Child company context : {res}")

        res = json.loads(self.sale_journal_accountant_context.kanban_dashboard_graph)
        self.assertEqual(len(res[0].get("values")), 0, f"Child company context : {res}")

    def test_02_dashboard_in_fiscal_mother(self):
        self.user_accountant.company_id = self.mother_company
        res = json.loads(self.sale_journal_accountant_context.kanban_dashboard)
        self.assertEqual(res.get("number_draft"), 0, f"Mother company context : {res}")
        self.assertEqual(
            res.get("number_waiting"), 0, f"Mother company context : {res}"
        )
        self.assertEqual(res.get("entries_count"), 0, f"Mother company context : {res}")

        res = json.loads(self.sale_journal_accountant_context.kanban_dashboard_graph)
        self.assertEqual(
            len(res[0].get("values")), 6, f"Mother company context : {res}"
        )
