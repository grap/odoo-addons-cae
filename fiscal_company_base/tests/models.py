from odoo import fields, models


class ModelFiscalCompanyChangeFilteredMixin(models.Model):
    _name = "model.fiscal.company.change.filtered.mixin"
    _description = "model.fiscal.company.change.filtered.mixin"
    _inherit = ["fiscal.company.change.filtered.mixin"]

    company_id = fields.Many2one(comodel_name="res.company")


class ModelFiscalCompanyChangeSearchDomainMixin(models.Model):
    _name = "model.fiscal.company.change.search.domain.mixin"
    _description = "model.fiscal.company.change.search.domain.mixin"
    _inherit = ["fiscal.company.change.search.domain.mixin"]

    company_id = fields.Many2one(comodel_name="res.company")


class ModelFiscalCompanyCheckCompanyMixinFiscalMother(models.Model):
    _name = "model.fiscal.company.check.company.mixin.fiscal.mother"
    _description = "model.fiscal.company.change.search.domain.mixin"
    _inherit = ["fiscal.company.check.company.mixin"]

    _fiscal_company_forbid_fiscal_type = ["fiscal_mother"]

    company_id = fields.Many2one(comodel_name="res.company")


class ModelFiscalCompanyPropagateChildCompanyMixin(models.Model):
    _name = "model.fiscal.company.propagate.child.company.mixin"
    _description = "fiscal.company.propagate.child.company.mixin"
    _inherit = ["fiscal.company.propagate.child.company.mixin"]

    company_id = fields.Many2one(comodel_name="res.company")

    company_dependent_field = fields.Char(company_dependent=True)

    def _fiscal_property_creation_list(self):
        return ["company_dependent_field"]


# pylint: disable=R8180
class ModelFiscalCompanyPropagateChildCompanyMixinResCompany(models.Model):
    _inherit = "res.company"

    def _get_model_from_properties_propagation(self):
        res = super()._get_model_from_properties_propagation()
        res += ["model.fiscal.company.propagate.child.company.mixin"]
        return res


class ModelWithCompany(models.Model):
    _name = "model.with.company"
    _description = "model.with.company"

    def with_company_disabled(self, company):
        return self.with_context(
            fiscal_company_disable_switch_company=True
        ).with_company(company)

    def with_company_enabled(self, company):
        return self.with_context(
            fiscal_company_disable_switch_company=False
        ).with_company(company)
