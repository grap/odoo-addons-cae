# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class IncludeFiscalCompanySearchMixin(models.AbstractModel):
    """ This abstract change the _search features for models.

    if a domain contain a ('company_id', '=', company_id)
    it will be replace by ('company_id', 'in', [company_id, fiscal_company_id])
    """

    _name = 'include.fiscal.company.search.mixin'
    _description = "Include Fiscal Company Search Mixin"

    @api.model
    def _include_fiscal_company_domain(self, domain):
        new_domain = []
        ResCompany = self.env['res.company']

        for item in domain:
            if (
                    isinstance(item, list)
                    or isinstance(item, tuple)
                    ) and item[0] == 'company_id':
                if isinstance(item[2], list):
                    old_company_ids = [item[2]]
                else:
                    old_company_ids = item[2]

                new_company_ids = ResCompany.browse(
                    old_company_ids).mapped('fiscal_company_id').ids

                if item[1] in ["=", "in"]:
                    new_operator = "in"
                elif item[1] in ["!=", "not in"]:
                    new_operator = "not in"
                else:
                    raise NotImplementedError("Not implemented operator")

                new_item = ("company_id", new_operator, new_company_ids)
                new_domain.append(new_item)
            else:
                new_domain.append(item)
        return new_domain

    @api.model
    def _search(
            self, args, offset=0, limit=None, order=None, count=False,
            access_rights_uid=None):
        new_args = self._include_fiscal_company_domain(args)
        return super()._search(
            new_args, offset=offset, limit=limit, order=order, count=count,
            access_rights_uid=access_rights_uid)
