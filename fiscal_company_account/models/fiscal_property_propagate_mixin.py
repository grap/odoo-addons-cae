# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class FiscalPropertyPropagateMixin(models.AbstractModel):
    _name = 'fiscal.property.propagate.mixin'
    _description = "Fiscal Property Propagation Features Mixin"

    @api.model
    def _fiscal_property_creation_list(self):
        """Overload me to define property fields to create to a new
        fiscal company
        """
        return []

    @api.multi
    def _fiscal_property_propagation_list(self):
        """Overload me to define property fields to propagate to all
        fiscal company.
        """
        self.ensure_one()
        return []

    # Overload Section
    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._propagate_fiscal_property_to_all_companies(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        self._propagate_fiscal_property_to_all_companies(vals)
        return res

    # Custom Function
    @api.multi
    def _propagate_fiscal_property_to_all_companies(self, vals):
        """
        Propagate a property of objects of for all fiscal
        childs of a mother company
        """
        IrModelFields = self.env['ir.model.fields']
        IrProperty = self.env['ir.property']
        company_id = self.env.context.get('force_company', False)
        if company_id:
            current_company = self.env['res.company'].browse(company_id)
        else:
            current_company = self.env.user.company_id

        if current_company.fiscal_type not in\
                ('fiscal_child', 'fiscal_mother'):
            return True

        for obj in self:
            property_name_list = [
                x for x in obj._fiscal_property_propagation_list()
                if x in vals]
            for property_name in property_name_list:
                property_value = vals[property_name]

                # Get fields information
                field = IrModelFields.search([
                    ('model', '=', self._name),
                    ('name', '=', property_name),
                ])[0]

                # Get all companies and remove the current company which
                # property has been just written
                company_ids =\
                    current_company.fiscal_company_id.fiscal_child_ids.ids
                company_ids.remove(current_company.id)

                # Delete all property
                domain = [
                    ('res_id', '=', '%s,%s' % (self._name, obj.id)),
                    ('fields_id', '=', field.id),
                    ('company_id', 'in', company_ids)]
                properties = IrProperty.search(domain)
                properties.unlink()

                # Create property for all fiscal childs
                if property_value:
                    for company_id in company_ids:
                        IrProperty.create({
                            'name': property_name,
                            'res_id': '%s,%s' % (self._name, obj.id),
                            'value': property_value,
                            'fields_id': field.id,
                            'type': field.ttype,
                            'company_id': company_id,
                        })
