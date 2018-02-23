# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestBaseFiscalCompany(TransactionCase):
    """Tests for 'Base Fiscal Company' Module"""

    # Overload Section
    def setUp(self):
        super(TestBaseFiscalCompany, self).setUp()

        self.user_obj = self.env['res.users']
        self.company_obj = self.env['res.company']
        self.mother_company = self.env.ref(
            'base_fiscal_company.company_fiscal_mother')
        self.base_company = self.env.ref('base.main_company')
        self.accountant_user = self.env.ref(
            'base_fiscal_company.user_accountant')

        self._fix_mail_bug("DROP")

    def tearDown(self):
        self.cr.rollback()
        self._fix_mail_bug("SET")
        super(TestBaseFiscalCompany, self).tearDown()

    # Test Section
    def test_01_res_users_propagate_access_right_create(self):
        """[Functional Test] A new user with access to mother company must
         have access to child companies"""
        new_user = self.user_obj.create({
            'name': 'new_user',
            'login': 'new_user@odoo.com',
            'company_id': self.mother_company.id,
            'company_ids': [(4, self.mother_company.id)]})
        self.assertEqual(
            len(new_user.company_ids),
            len(self.mother_company.fiscal_child_ids),
            "Affect a mother company to a new user must give access right"
            "to the childs companies")

    def test_02_res_users_propagate_access_right_write(self):
        """[Functional Test] Give access to a mother company must give acces
        to the child companies"""
        new_user = self.user_obj.create({
            'name': 'new_user',
            'login': 'new_user@odoo.com',
            'company_id': self.base_company.id,
            'company_ids': [(4, self.base_company.id)]})
        new_user.write({'company_ids': [(4, self.mother_company.id)]})
        self.assertEqual(
            len(new_user.company_ids),
            len(self.mother_company.fiscal_child_ids) + 1,
            "Give access to a mother company must give access"
            "to the child companies")

    def test_03_res_company_check_contraint_fail_01(self):
        """[Contraint Test] Try to create a company with
        'fiscal_type != 'child' and and a mother company."""
        with self.assertRaises(ValidationError):
            self.company_obj.create({
                'name': 'new_company',
                'fiscal_type': 'normal',
                'fiscal_company_id': self.mother_company.id})

    def test_04_res_company_check_contraint_fail_02(self):
        """[Contraint Test] Try to create a company with
        'fiscal_type != 'child' and and a mother company."""
        with self.assertRaises(ValidationError):
            self.company_obj.create({
                'name': 'new_company_1',
                'fiscal_type': 'fiscal_mother',
                'fiscal_company_id': self.mother_company.id})
        with self.assertRaises(ValidationError):
            self.company_obj.create({
                'name': 'new_company_2',
                'fiscal_type': 'normal',
                'fiscal_company_id': self.mother_company.id})

    def test_05_res_company_check_contraint_fail_03(self):
        """[Contraint Test] Try to create a company with
        'fiscal_type = 'child' without a mother company."""
        with self.assertRaises(ValidationError):
            self.company_obj.create({
                'name': 'new_company',
                'fiscal_type': 'fiscal_child',
                'fiscal_company_id': False})

    def test_06_res_company_create_child_propagate_success(self):
        """[Contraint Test] Create a child company and check propagation."""
        new_company = self.company_obj.create({
            'name': 'new_company',
            'fiscal_type': 'fiscal_child',
            'fiscal_company_id': self.mother_company.id})
        new_access = self.accountant_user.company_ids.filtered(
            lambda x: x.id == new_company.id).ids
        self.assertEqual(
            new_access, [new_company.id],
            "Existing user must have access to the new child company.")

    def test_07_res_company_write_child_propagate_success(self):
        """[Contraint Test] Create and write a child company and check
         propagation."""
        new_company = self.company_obj.create({
            'name': 'new_company',
            'fiscal_type': 'normal'})
        new_company.write({
            'fiscal_type': 'fiscal_child',
            'fiscal_company_id': self.mother_company.id})

        new_access = self.accountant_user.company_ids.filtered(
            lambda x: x.id == new_company.id).ids
        self.assertEqual(
            new_access, [new_company.id],
            "Existing user must have access to the new child company.")

    # Private Section
    def _fix_mail_bug(self, function):
        """ Tests are failing on a database with 'mail' module installed,
        Because the load of the registry in TransactionCase seems to be bad.
        To be sure, run "print self.registry('res.partner')._defaults and see
        that the mandatory field 'notify_email' doesn't appear.
        So this is a monkey patch that drop and add not null constraint
        to make that tests working."""
        self.cr.execute("""
            SELECT A.ATTNAME
                FROM PG_ATTRIBUTE A, PG_CLASS C
                WHERE A.ATTRELID = C.OID
                AND A.ATTNAME = 'notify_email'
                AND C.relname= 'res_partner';""")
        if self.cr.fetchone():
            self.cr.execute("""
                ALTER TABLE res_partner
                    ALTER COLUMN notify_email
                    %s NOT NULL;""" % (function))
