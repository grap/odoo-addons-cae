# -*- coding: utf-8 -*-
# Copyright (C) 2017-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, exceptions, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # Column Section
    product_default_code_sequence_id = fields.Many2one(
        comodel_name='ir.sequence', readonly=True)

    use_default_code_sequence = fields.Boolean()

    # Constrains
    @api.constrains('use_default_code_sequence', 'fiscal_code')
    def _check_use_default_code_sequence(self):
        for company in self:
            if not company.fiscal_code and company.use_default_code_sequence:
                raise exceptions.ValidationError(_(
                    "You should set fiscal_code if you want to use default"
                    " code sequence for products."))

    # Overload Section
    @api.model
    def create(self, vals):
        res = super(ResCompany, self).create(vals)
        res._create_product_default_code_sequence()
        return res

    @api.multi
    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        if 'fiscal_code' in vals:
            self._create_product_default_code_sequence()
        return res

    # Custom Section
    @api.multi
    def _create_product_default_code_sequence(self):
        sequence_obj = self.env['ir.sequence']
        for company in self:
            if company.fiscal_code:
                vals = company._prepare_default_code_sequence()
                if not company_id.product_default_code_sequence_id:
                    company.product_default_code_sequence_id =\
                        sequence_obj.create(vals)
                else:
                    company.product_default_code_sequence_id.write({
                        'name': vals['name'],
                        'prefix': vals['prefix'],
                    })

    @api.multi
    def _prepare_product_default_code_sequence(vals):
        self.ensure_one()
        return {
            'name': '%s - Default Code for Products' % (self.fiscal_code),
            'fiscal_code': 'product_product.default_code',
            'company_id': self.id,
            'prefix': '%s-' % (self.fiscal_code),
            'padding': 6,
        }
