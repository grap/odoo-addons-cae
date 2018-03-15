# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from openerp.osv.orm import Model


class ProductPricelist(Model):
    _inherit = 'product.pricelist'

    # Overload Section
    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False):
        """Add a required modifiers on the field company_id"""
        res = super(ProductPricelist, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar)
        if view_type in ('form', 'tree')\
                and 'company_id' in res['fields']:
            res['fields']['required'] = True
            doc = etree.XML(res['arch'])
            node = doc.xpath("//field[@name='company_id']")[0]
            node.set('modifiers', '{"required": true}')
            res['arch'] = etree.tostring(doc)
        return res
