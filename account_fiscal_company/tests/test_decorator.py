# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase

from odoo.addons.base_fiscal_company.fix_test import fix_required_field


class TestDecorator(TransactionCase):
    """Tests for Account Fiscal Company Module (Decorator)"""

    def setUp(self):
        super(TestDecorator, self).setUp()
        fix_required_field(self, 'DROP')

    def tearDown(self):
        self.cr.rollback()
        fix_required_field(self, 'SET')
        super(TestDecorator, self).tearDown()
