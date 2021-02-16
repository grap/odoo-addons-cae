# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Category - Global Account Settings",
    "version": "12.0.1.0.2",
    "summary": "Propagate Accouting settings of product categories"
    " for all the companies",
    "category": "Accounting",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": ["stock_account", "fiscal_company_account"],
    "data": ["views/view_product_category.xml"],
    "demo": ["demo/account_chart_template.xml", "demo/account_account_template.xml"],
    "installable": True,
}
