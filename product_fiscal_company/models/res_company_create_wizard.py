# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import TransientModel
from openerp.tools.translate import _


class ResCompanyCreateWizard(TransientModel):
    _inherit = 'res.company.create.wizard'

    def begin(self, cr, uid, id, context=None):
        property_obj = self.pool['ir.property']
        model_obj = self.pool['ir.model.data']
        pricelist_obj = self.pool['product.pricelist']
        version_obj = self.pool['product.pricelist.version']
        item_obj = self.pool['product.pricelist.item']

        res = super(ResCompanyCreateWizard, self).begin(
            cr, uid, id, context=context)

        wizard = self.browse(cr, uid, id, context=context)

        # creating Sale Pricelist
        pricelist_id = pricelist_obj.create(cr, uid, {
            'name': _('%s - Default Public Pricelist') % (wizard.code),
            'currency_id': wizard.company_id.currency_id.id,
            'type': 'sale',
            'company_id': wizard.company_id.id,
        }, context=context)

        version_id = version_obj.create(cr, uid, {
            'name': _('%s - Default Public Pricelist Version') % (wizard.code),
            'pricelist_id': pricelist_id,
        }, context=context)

        item_obj.create(cr, uid, {
            'name': _('%s - Default Public Pricelist Line') % (wizard.code),
            'price_version_id': version_id,
            'base': 1,
        }, context=context)

        # Create Properties
        property_obj.create(cr, uid, {
            'name': 'property_product_pricelist',
            'company_id': wizard.company_id.id,
            'fields_id': model_obj.get_object_reference(
                cr, uid, 'product',
                'field_res_partner_property_product_pricelist')[1],
            'type': 'many2one',
            'value_reference': 'product.pricelist,%s' % (pricelist_id),
        }, context=context)

        res.update({
            'public_pricelist_id': pricelist_id,
        })
        return res
