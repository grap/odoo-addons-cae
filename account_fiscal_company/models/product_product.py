# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'fiscal.property.propagate.mixin']

    @api.model
    def _fiscal_property_propagation_list(self):
        res = super(ProductProduct, self)._fiscal_property_propagation_list()
        return res + [
            'property_account_expense',
            'property_account_income',
        ]
