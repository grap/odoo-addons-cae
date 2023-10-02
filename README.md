
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/grap/odoo-addons-cae/actions/workflows/pre-commit.yml/badge.svg?branch=12.0)](https://github.com/grap/odoo-addons-cae/actions/workflows/pre-commit.yml?query=branch%3A12.0)
[![Build Status](https://github.com/grap/odoo-addons-cae/actions/workflows/test.yml/badge.svg?branch=12.0)](https://github.com/grap/odoo-addons-cae/actions/workflows/test.yml?query=branch%3A12.0)
[![codecov](https://codecov.io/gh/grap/odoo-addons-cae/branch/12.0/graph/badge.svg)](https://codecov.io/gh/grap/odoo-addons-cae)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

# Odoo Modules for CAE (Cooperative d'Activité et d'Emploi)

 This project aim to deal with modules related to manage CAE in Odoo.
More information about CAE [FR]
- https://fr.wikipedia.org/wiki/Coopérative_d'activités_et_d'emploi
- http://www.cooperer.coop/
- http://www.copea.fr/

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fiscal_company_account](fiscal_company_account/) | 12.0.1.1.0 |  | Glue Module between CAE and Account modules
[fiscal_company_base](fiscal_company_base/) | 12.0.1.2.3 |  | Manage CAE (Cooperatives of Activities and Employment)
[fiscal_company_company_wizard_account](fiscal_company_company_wizard_account/) | 12.0.1.1.0 |  | Glue Module between CAE and Company Wizard - Account modules
[fiscal_company_company_wizard_base](fiscal_company_company_wizard_base/) | 12.0.1.1.0 |  | Glue Module between CAE and Company Wizard - Base modules
[fiscal_company_point_of_sale](fiscal_company_point_of_sale/) | 12.0.1.2.1 |  | Glue Module between CAE and Point of Sale modules
[fiscal_company_product](fiscal_company_product/) | 12.0.1.1.1 |  | Glue Module between CAE and Product modules
[fiscal_company_sale](fiscal_company_sale/) | 12.0.1.1.0 |  | Glue Module between CAE and Sale modules
[fiscal_company_sales_team](fiscal_company_sales_team/) | 12.0.1.1.0 |  | Glue Module between CAE and Sales Team modules
[product_category_global_account_setting](product_category_global_account_setting/) | 12.0.1.1.1 |  | Propagate Accouting settings of product categories for all the companies
[recurring_consignment_fiscal_company](recurring_consignment_fiscal_company/) | 12.0.1.1.1 |  | Glue module for Recurring Consignment and fiscal company modules

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to GRAP
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----

## About GRAP

<p align="center">
   <img src="http://www.grap.coop/wp-content/uploads/2016/11/GRAP.png" width="200"/>
</p>

GRAP, [Groupement Régional Alimentaire de Proximité](http://www.grap.coop) is a
french company which brings together activities that sale food products in the
region Rhône Alpes. We promote organic and local food, social and solidarity
economy and cooperation.

The GRAP IT Team promote Free Software and developp all the Odoo modules under
AGPL-3 Licence.

You can find all these modules here:

* on the [OCA Apps Store](https://odoo-community.org/shop?&search=GRAP)
* on the [Odoo Apps Store](https://www.odoo.com/apps/modules/browse?author=GRAP).
* on [Odoo Code Search](https://odoo-code-search.com/ocs/search?q=author%3AOCA+author%3AGRAP)

You can also take a look on the following repositories:

* [grap-odoo-incubator](https://github.com/grap/grap-odoo-incubator)
* [grap-odoo-business](https://github.com/grap/grap-odoo-business)
* [grap-odoo-business-supplier-invoice](https://github.com/grap/grap-odoo-business-supplier-invoice)
* [odoo-addons-logistics](https://github.com/grap/odoo-addons-logistics)
* [odoo-addons-cae](https://github.com/grap/odoo-addons-cae)
* [odoo-addons-intercompany-trade](https://github.com/grap/odoo-addons-intercompany-trade)
* [odoo-addons-multi-company](https://github.com/grap/odoo-addons-multi-company)
* [odoo-addons-company-wizard](https://github.com/grap/odoo-addons-company-wizard)
