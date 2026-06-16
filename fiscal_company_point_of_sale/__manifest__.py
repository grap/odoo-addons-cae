# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "CAE - Point Of Sale",
    "version": "16.0.2.0.0",
    "category": "CAE",
    "summary": "Glue Module between CAE and Point of Sale modules",
    "author": "GRAP",
    "website": "https://github.com/grap/odoo-addons-cae",
    "license": "AGPL-3",
    "depends": [
        # Odoo
        "point_of_sale",
        # GRAP
        "fiscal_company_base",
        "fiscal_company_product",
        "fiscal_company_account",
    ],
    "demo": [
        "demo/pos_payment_method.xml",
        "demo/pos_config.xml",
    ],
    "installable": True,
    "auto_install": True,
}
