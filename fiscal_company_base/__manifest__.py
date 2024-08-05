# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "CAE - Base",
    "version": "16.0.1.0.0",
    "category": "CAE",
    "summary": "Manage CAE (Cooperatives of Activities and Employment)",
    "author": "GRAP",
    "website": "https://github.com/grap/odoo-addons-cae",
    "license": "AGPL-3",
    "depends": [
        "base",
        # Dependency added to have the possibility to create demo user,
        # without "notification_type" error
        "mail",
    ],
    "data": [
        # "security/ir_rule.xml",
        "views/view_res_company.xml",
    ],
    "demo": [
        "demo/res_partner_company.xml",
        "demo/res_partner_users.xml",
        "demo/res_partner.xml",
        "demo/res_groups.xml",
    ],
    "installable": True,
}
