from odoo import fields, models


class ModelFiscalCompanyChangeSearchDomainMixin(models.Model):
    _name = "model.fiscal.company.change.search.domain.mixin"
    _inherit = ["fiscal.company.change.search.domain.mixin"]

    _description = "model.fiscal.company.change.search.domain.mixin"

    company_id = fields.Many2one(comodel_name="res.company")


class FiscalCompanyCheckCompanyMixinFiscalMother(models.Model):
    _name = "model.fiscal.company.check.company.mixin.fiscal.mother"
    _inherit = ["fiscal.company.check.company.mixin"]

    _description = "model.fiscal.company.change.search.domain.mixin"

    _fiscal_company_forbid_fiscal_type = ["fiscal_mother"]

    company_id = fields.Many2one(comodel_name="res.company")
