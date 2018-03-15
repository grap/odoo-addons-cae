# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class PricelistPartnerinfo(models.Model):
    _inherit = 'pricelist.partnerinfo'

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', readonly=True,
        related='suppinfo_id.company_id')
