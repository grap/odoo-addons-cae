# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


_FIELD_LIST = [
    ('res_partner', 'notify_email'),
    ('res_partner', 'invoice_warn'),
    ('res_partner', 'sale_warn'),
    ('res_partner', 'picking_warn'),
    ('res_partner', 'purchase_warn'),
]


def fix_required_field(env, function):
    """ Tests are failing on a database with some modules installed like 'mail'
    because the load of the registry in TransactionCase seems to be bad.
    To be sure, run "print self.registry('res.partner')._defaults and see
    that the mandatory field 'notify_email' doesn't appear.
    So this is a monkey patch that drop and add not null constraint
    to make the tests working.
    arguments : function.
        'DROP' at the beginning of the test setUp(self)
        'SET' at the end of the test tearDown(self)
    """
    for table_name, field_name in _FIELD_LIST:
        env.cr.execute("""
            SELECT A.ATTNAME
                FROM PG_ATTRIBUTE A, PG_CLASS C
                WHERE A.ATTRELID = C.OID
                AND A.ATTNAME = '%s'
                AND C.relname= '%s';""" % (field_name, table_name))
        if env.cr.fetchone():
            env.cr.execute("""
                ALTER TABLE %s
                    ALTER COLUMN %s
                    %s NOT NULL;""" % (table_name, field_name, function))
