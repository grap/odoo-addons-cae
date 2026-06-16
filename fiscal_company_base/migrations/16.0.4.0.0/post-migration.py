# Copyright (C) 2024-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


# pylint: disable=W8150
from odoo.addons.fiscal_company_base import hooks


def migrate(cr, version):
    hooks._toggle_standard_rules(cr, False)
