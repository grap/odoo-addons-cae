# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase

class TestBaseFiscalCompany(TransactionCase):
    """Tests for 'Base Fiscal Company' Module"""

    # Overload Section
    def setUp(self):
        super(TestBaseFiscalCompany, self).setUp()

        # Get Registries
        self.user_obj = self.env['res.users']
        self.company_obj = self.env['res.company']

        # Get ids from xml_ids
#        self.accountant_user_id = self.imd_obj.get_object_reference(
#            self.cr, self.uid,
#            'base_fiscal_company', 'user_accountant')[1]
        self.mother_company = self.env.ref(
            'base_fiscal_company.company_fiscal_mother')
#        self.base_company_id = self.imd_obj.get_object_reference(
#            self.cr, self.uid,
#            'base', 'main_company')[1]
#        self.fix_mail_bug("DROP")


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

##    def test_02_res_users_propagate_access_right_write(self):
##        """[Functional Test] Give access to a mother company must give acces
##        to the child companies"""
##        cr, uid = self.cr, self.uid
##        ru_id = self.ru_obj.create(cr, uid, {
##            'name': 'new_user',
##            'login': 'new_user@odoo.com',
##            'company_id': self.base_company_id,
##            'company_ids': [(4, self.base_company_id)]})
##        self.ru_obj.write(cr, uid, [ru_id], {
##            'company_ids': [(4, self.mother_company_id)]})
##        ru = self.ru_obj.browse(cr, uid, ru_id)
##        rc = self.rc_obj.browse(cr, uid, self.mother_company_id)
##        self.assertEqual(
##            len(ru.company_ids), len(rc.fiscal_childs) + 1,
##            "Give access to a mother company must give acces"
##            "to the child companies")

##    def test_03_res_company_check_contraint_fail_01(self):
##        """[Contraint Test] Must Fail. Try to create a company with
##        'fiscal_type != 'child' and and a mother company."""
##        cr, uid = self.cr, self.uid
##        exception_raised = False
##        try:
##            self.rc_obj.create(cr, uid, {
##                'name': 'new_company',
##                'fiscal_type': 'normal',
##                'fiscal_company': self.mother_company_id})
##        except:
##            exception_raised = True
##        self.assertEqual(exception_raised, True, "Must raise an error.")

##    def test_04_res_company_check_contraint_fail_02(self):
##        """[Contraint Test] Must Fail. Try to create a company with
##        'fiscal_type != 'child' and and a mother company."""
##        cr, uid = self.cr, self.uid
##        exception_raised = False
##        try:
##            self.rc_obj.create(cr, uid, {
##                'name': 'new_company',
##                'fiscal_type': 'fiscal_mother',
##                'fiscal_company': self.mother_company_id})
##        except:
##            exception_raised = True
##        self.assertEqual(exception_raised, True, "Must raise an error.")

##    def test_05_res_company_check_contraint_fail_03(self):
##        """[Contraint Test] Must Fail. Try to create a company with
##        'fiscal_type = 'child' without a mother company."""
##        cr, uid = self.cr, self.uid
##        exception_raised = False
##        try:
##            self.rc_obj.create(cr, uid, {
##                'name': 'new_company',
##                'fiscal_type': 'fiscal_child',
##                'fiscal_company': None})
##        except:
##            exception_raised = True
##        self.assertEqual(exception_raised, True, "Must raise an error.")

##    def test_06_res_company_create_child_propagate_success(self):
##        """[Contraint Test] Create a child company and check propagation."""
##        cr, uid = self.cr, self.uid
##        rc_id = self.rc_obj.create(cr, uid, {
##            'name': 'new_company',
##            'fiscal_type': 'fiscal_child',
##            'fiscal_company': self.mother_company_id})
##        ru = self.ru_obj.browse(cr, uid, self.accountant_user_id)
##        found = False
##        for rc in ru.company_ids:
##            if rc.id == rc_id:
##                found = True
##        self.assertEqual(
##            found, True,
##            "Existing user must have access to the new child company.")

##    def test_06_res_company_write_child_propagate_success(self):
##        """[Contraint Test] Create and write a child company and check
##         propagation."""
##        cr, uid = self.cr, self.uid
##        rc_id = self.rc_obj.create(cr, uid, {
##            'name': 'new_company',
##            'fiscal_type': 'normal'})
##        self.rc_obj.write(cr, uid, [rc_id], {
##            'fiscal_type': 'fiscal_child',
##            'fiscal_company': self.mother_company_id})
##        ru = self.ru_obj.browse(cr, uid, self.accountant_user_id)
##        found = False
##        for rc in ru.company_ids:
##            if rc.id == rc_id:
##                found = True
##        self.assertEqual(
##            found, True,
##            "Existing user must have access to the new child company.")

#    # TODO: FIXME
#    def fix_mail_bug(self, function):
#        """ Tests are failing on a database with 'mail' module installed,
#        Because the load of the registry in TransactionCase seems to be bad.
#        To be sure, run "print self.registry('res.partner')._defaults and see
#        that the mandatory field 'notify_email' doesn't appear.
#        So this is a monkey patch that drop and add not null constraint
#        to make that tests working."""
#        self.cr.execute("""
#            SELECT A.ATTNAME
#                FROM PG_ATTRIBUTE A, PG_CLASS C
#                WHERE A.ATTRELID = C.OID
#                AND A.ATTNAME = 'notify_email'
#                AND C.relname= 'res_partner';""")
#        if self.cr.fetchone():
#            self.cr.execute("""
#                ALTER TABLE res_partner
#                    ALTER COLUMN notify_email
#                    %s NOT NULL;""" % (function))

#    def tearDown(self):
#        self.cr.rollback()
#        self.fix_mail_bug("SET")
#        super(TestBaseFiscalCompany, self).tearDown()
