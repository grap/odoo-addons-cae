# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Overload Section
    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        res._set_default_code()
        return res

    # Custom Section
    @api.multi
    def _set_default_code(self):
        ir_sequence_obj = self.env['ir.sequence']
        for product in self:
            if product.company_id and\
                    product.company_id.use_default_code_sequence:
                product.default_code = ir_sequence_obj.get(
                    'product_product.default_code')
