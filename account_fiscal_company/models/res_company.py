# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author:
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model
from openerp.addons.account_fiscal_company.account_parameters \
    import propagate_properties_to_new_fiscal_child


class ResCompany(Model):
    _inherit = 'res.company'

    def create(self, cr, uid, vals, context=None):
        pc_obj = self.pool['product.category']
        res = super(ResCompany, self).create(
            cr, uid, vals, context=context)
        if vals.get('fiscal_type') == 'fiscal_child':
            # Apply all product category properties to the new company
            for property_name in pc_obj._PRODUCT_CATEGORY_FISCAL_PROPERTY_LIST:
                propagate_properties_to_new_fiscal_child(
                    self.pool, cr, uid,
                    vals.get('fiscal_company'),
                    res,
                    'product.category',
                    property_name,
                    context=context)
        return res
