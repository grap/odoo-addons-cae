# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class FiscalPropertyPropagateMixin(models.AbstractModel):
    _name = 'fiscal.property.propagate.mixin'

    @api.model
    def _fiscal_property_propagation_list(self):
        """Overload me to define property field to propagate to all
        fiscal company.
        """
        return []

    # Overload Section
    @api.model
    def create(self, vals):
        res = super(FiscalPropertyPropagateMixin, self).create(vals)
        res._propagate_fiscal_property_to_all_companies(vals, True)
        return res

    @api.multi
    def write(self, vals):
        res = super(FiscalPropertyPropagateMixin, self).write(vals)
        self._propagate_fiscal_property_to_all_companies(vals, False)
        return res

    # Custom Function
    @api.multi
    def _propagate_fiscal_property_to_all_companies(self, vals, creation):
        field_obj = self.env['ir.model.fields']
        property_obj = self.env['ir.property']
        current_company = self.env.user.company_id

        if current_company.fiscal_type in ('fiscal_child', 'fiscal_mother'):
            property_name_list = [
                x for x in self._fiscal_property_propagation_list()
                if x in vals]
            for property_name in property_name_list:
                property_value = vals[property_name]

                # Get fields information
                domain = [
                    ('model', '=', self._name),
                    ('name', '=', property_name),
                ]
                field = field_obj.search(domain)[0]

                # Get all companies and remove the current company which
                # property has been just written
                company_ids =\
                    current_company.fiscal_company_id.fiscal_child_ids.ids
                company_ids.remove(current_company.id)

                for obj in self:
                    # Delete all property
                    domain = [
                        ('res_id', '=', '%s,%s' % (self._name, obj.id)),
                        ('fields_id', '=', field.id),
                        ('company_id', 'in', company_ids)]
                    properties = property_obj.search(domain)
                    properties.unlink()

                    # Create property for all fiscal childs
                    if property_value:
                        for company_id in company_ids:
                            property_obj.create({
                                'name': property_name,
                                'res_id': '%s,%s' % (self._name, obj.id),
                                'value': property_value,
                                'fields_id': field.id,
                                'type': field.ttype,
                                'company_id': company_id,
                            })
