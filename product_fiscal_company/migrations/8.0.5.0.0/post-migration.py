# -*- coding: utf-8 -*-
# Copyright (C) 2017-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

from openerp.modules.registry import RegistryManager
from openerp import SUPERUSER_ID

logger = logging.getLogger('product_fiscal_company')


@openupgrade.migrate()
def migrate(cr, version):
    registry = RegistryManager.get(cr.dbname)
    company_obj = registry['res.company']
    product_obj = registry['product.product']
    user_obj = registry['res.users']
    company_ids = company_obj.search(cr, SUPERUSER_ID, [('code', '!=', False)])
    for company_id in company_ids:
        user_obj.write(
            cr, SUPERUSER_ID, [SUPERUSER_ID], {'company_id': company_id})
        company_obj._create_default_code_sequence(
            cr, SUPERUSER_ID, [company_id])
        active_product_ids = product_obj.search(
            cr, SUPERUSER_ID,
            [('active', '=', True), ('company_id', '=', company_id)])
        inactive_product_ids = product_obj.search(
            cr, SUPERUSER_ID,
            [('active', '=', False), ('company_id', '=', company_id)])
        product_ids = active_product_ids + inactive_product_ids
        logger.info(
            "Setting Product default code for %d products", len(product_ids))
        product_obj._set_default_code(cr, SUPERUSER_ID, product_ids)
