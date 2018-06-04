# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    _PROPERTY_MODEL_LIST = [
        'res.partner', 'product.template', 'product.category']

    @api.model
    def create(self, vals):
        res = super(ResCompany, self).create(vals)
        if vals.get('fiscal_type') == 'fiscal_child':
            res._propagate_properties_to_new_fiscal_child()
        return res

    @api.multi
    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        if vals.get('fiscal_type') == 'fiscal_child':
            res._propagate_properties_to_new_fiscal_child()
        return res

    @api.multi
    def _propagate_properties_to_new_fiscal_child(self):
        """
        Propagate all properties of objects (product, category) for a new
        fiscal company
        """
        field_obj = self.env['ir.model.fields']
        property_obj = self.env['ir.property']
        for company in self:
            for model_name in self._PROPERTY_MODEL_LIST:
                model_obj = self.env[model_name]
                property_name_list = model_obj._fiscal_property_creation_list()
                for property_name in property_name_list:
                    field = field_obj.search([
                        ('model', '=', model_name),
                        ('name', '=', property_name),
                    ])[0]
                    # Get existing properties
                    existing_properties = property_obj.search([
                        ('fields_id', '=', field.id),
                        ('company_id', '=', company.fiscal_company_id.id),
                    ])
                    # Duplicate properties for the new fiscal childc company
                    for existing_property in existing_properties:
                        new_property = existing_property.copy(default={
                            'company_id': company.id,
                        })
