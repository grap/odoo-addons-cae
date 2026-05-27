# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class FiscalCompanyPropagateChildCompanyMixin(models.AbstractModel):
    """This abstract allow to propagate properties of mother companies
    in child companies context.
    - When creating a new child company, all the properties defined
      at mother company will be set in the new child company.
    - When setting a value on item defined related to mother company
      the property value will be propagated to all the companies
      (mother & children)
    """

    _name = "fiscal.company.propagate.child.company.mixin"
    _description = "Fiscal Company : Propagate in Child Company Mixin"

    @api.model
    def _fiscal_property_creation_list(self):
        """Overload me to define property fields to create to a new
        fiscal company
        """
        return []

    @api.model_create_multi
    def create(self, vals_list):
        items = super().create(vals_list)
        for item, vals in zip(items, vals_list, strict=True):
            if not item.company_id or item.company_id.fiscal_type != "fiscal_mother":
                continue
            item._propagate_property_to_all_fiscal_child_companies(vals)
        return items

    def write(self, vals):
        result = super().write(vals)
        if self.env.context.get("do_not_propagate_write_on_properties", False):
            return result
        for item in self.filtered(
            lambda x: x.company_id and x.company_id.fiscal_type == "fiscal_mother"
        ):
            item._propagate_property_to_all_fiscal_child_companies(vals)
        return result

    def _propagate_property_to_all_fiscal_child_companies(self, vals):
        self.ensure_one()
        fields = set(vals.keys()).intersection(self._fiscal_property_creation_list())
        if not fields:
            return

        new_vals = {k: v for k, v in vals.items() if k in fields}
        for company in self.company_id.fiscal_child_ids:
            if company == self.env.company:
                # skip current company, as the value is already written
                continue
            self.sudo().with_company(company.id).with_context(
                do_not_propagate_write_on_properties=True
            ).write(new_vals)
