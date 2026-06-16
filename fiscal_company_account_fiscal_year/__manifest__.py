# Copyright (C) 2024-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "CAE - Account Fiscal Year",
    "version": "16.0.3.0.0",
    "category": "CAE",
    "summary": "Glue Module between CAE and Account Fiscal year module",
    "author": "GRAP",
    "website": "https://github.com/grap/odoo-addons-cae",
    "license": "AGPL-3",
    "depends": [
        # OCA
        "account_fiscal_year",
        # GRAP
        "fiscal_company_account",
    ],
    "data": [
        "security/ir_rule.xml",
    ],
    "demo": [
        "demo/account_fiscal_year.xml",
    ],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "installable": True,
    "auto_install": True,
}
