# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ProductCategory(models.Model):
    _name = 'product.category'
    _inherit = ['product.category', 'fiscal.property.propagate.mixin']

    @api.model
    def _fiscal_property_propagation_list(self):
        res = super(ProductCategory, self)._fiscal_property_propagation_list()
        return res + [
            'property_account_income_categ_id',
            'property_account_expense_categ_id',
        ]
