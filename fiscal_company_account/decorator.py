# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import functools


# Private Function Section
def _get_fiscal_mother_company(self, operator, company_id):
    ResCompany = self.env['res.company']
    if operator != 'in':
        new_company_id = ResCompany.browse(
            company_id).fiscal_company_id.id
        return new_company_id
    else:
        new_company_ids = ResCompany.browse(
            company_id).mapped('fiscal_company_id').ids
        return new_company_ids


def _replace_company_id_tuple(self, arg):
    """
    replace ('company_id', operator, company_arg) by
        ('company_id', operator, company_arg.mapped('fiscal_company_id').ids)
    OR recursively call replace_company_id
    """
    if arg[0] == 'company_id':
        operator = arg[1]
        return (arg[0], operator, _get_fiscal_mother_company(
            self, operator, arg[2]))
    else:
        return tuple(
            _replace_company_id(self, arg[x]) for x in range(0, len(arg)))


def _replace_company_id_list(self, arg):
    """
    replace ['company_id', operator, company_arg] by
        ('company_id', operator, company_arg.mapped('fiscal_company_id').ids]
    OR recursively call replace_company_id
    """
    if arg[0] == 'company_id':
        operator = arg[1]
        return [arg[0], operator, _get_fiscal_mother_company(
            self, operator, arg[2])]
    return list(
        _replace_company_id(self, arg[x]) for x in range(0, len(arg)))


def _replace_company_id(self, arg):
    if 'company_id' in str(arg):
        if isinstance(arg, tuple):
            return _replace_company_id_tuple(self, arg)
        elif isinstance(arg, list):
            return _replace_company_id_list(self, arg)
        else:
            return arg
    else:
        return arg


# Decorators section
def switch_company(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        args2 = _replace_company_id(self, args)
        response = func(self, *args2, **kwargs)
        return response
    return wrapper
