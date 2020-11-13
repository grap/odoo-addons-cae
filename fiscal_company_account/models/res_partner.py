# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'fiscal.property.propagate.mixin']

    _FISCAL_PROPERTY_LIST = [
        'property_account_position_id',
        'property_account_payable_id',
        'property_account_receivable_id',
        'property_payment_term_id',
        'property_supplier_payment_term_id',
    ]

    @api.model
    def _fiscal_property_creation_list(self):
        res = super()._fiscal_property_creation_list()
        return res + self._FISCAL_PROPERTY_LIST

    @api.multi
    def _fiscal_property_propagation_list(self):
        self.ensure_one()
        res = super()._fiscal_property_propagation_list()
        # Propagation only for object that belong to the fiscal_mother
        # company
        if self.company_id.fiscal_type == 'fiscal_mother':
            res = res + self._FISCAL_PROPERTY_LIST
        return res

    # <dirty hack>
    # the reason of the following lines are :
    # property_account_position_id is a property
    # 1) using this field, a domain is automatically added by the orm / web
    # in the name_get for exemple:
    # ('company_id', 'in', (current_company, False))
    # this domain is not fixed for the time being, by any decorator
    # So the selection can not be done in a fiscal_company context
    # 2) also, we have to rewrite after a create, because the _inverse
    # function doesn't seems to work for properties, (only for create,
    # it works for regular write)
    @api.model
    def create(self, vals):
        res = super().create(vals)
        if "no_property_account_position_id" in vals.keys():
            res.write({
                "property_account_position_id":
                vals["no_property_account_position_id"],
            })
        return res

    no_property_account_position_id = fields.Many2one(
        string="Fiscal Position (*)",
        comodel_name="account.fiscal.position",
        domain=lambda x: x._domain_no_property_account_position_id(),
        compute="_compute_no_property_account_position_id",
        inverse="_inverse_no_property_account_position_id")

    def _domain_no_property_account_position_id(self):
        return [("company_id", "in", [
            self.env.user.company_id.id,
            self.env.user.company_id.fiscal_company_id.id,
            ])]

    def _compute_no_property_account_position_id(self):
        for partner in self:
            partner.no_property_account_position_id =\
                partner.property_account_position_id

    def _inverse_no_property_account_position_id(self):
        for partner in self:
            partner.property_account_position_id =\
                partner.no_property_account_position_id
    # </dirty Hack>
