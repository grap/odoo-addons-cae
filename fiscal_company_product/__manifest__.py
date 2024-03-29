# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "CAE - Product",
    "version": "12.0.1.1.1",
    "category": "CAE",
    "summary": "Glue Module between CAE and Product modules",
    "author": "GRAP",
    "website": "https://github.com/grap/odoo-addons-cae",
    "license": "AGPL-3",
    "depends": ["fiscal_company_base", "product"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/view_product_template.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_pricelist.xml",
        "demo/product_template.xml",
        "demo/product_product.xml",
    ],
    "installable": True,
    "auto_install": True,
}
