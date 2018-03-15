# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'fiscal.property.propagate.mixin']

    @api.model
    def _fiscal_property_creation_list(self):
        res = super(ProductTemplate, self)._fiscal_property_creation_list()
        return res + [
            'property_account_expense_id',
            'property_account_income_id',
        ]

    @api.multi
    def _fiscal_property_propagation_list(self):
        self.ensure_one()
        res = super(ProductTemplate, self)._fiscal_property_propagation_list()
        # Propagation only for object that belong to the fiscal_mother
        # company
        if self.company_id.fiscal_type == 'fiscal_mother':
            res = res + [
                'property_account_expense_id',
                'property_account_income_id',
            ]
        return res
