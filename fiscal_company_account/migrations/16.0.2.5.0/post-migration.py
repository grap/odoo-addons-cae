# Copyright 2024 ForgeFlow S.L. (http://www.forgeflow.com)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

# pylint: disable=W8150
from odoo.addons.fiscal_company_account import hooks


def migrate(cr, version):
    hooks._toggle_standard_rules(cr, False)
