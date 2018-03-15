# coding: utf-8
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import functools


def replace_company_id_tuple(self, arg):
    """
    replace ('company_id', operator, company_arg) by
        ('company_id', operator, company_arg.mapped('fiscal_company_id').ids
    OR recursively call replace_company_id
    """
    if arg[0] == 'company_id':
        operator = arg[1]
        if operator != 'in':
            new_company_id = self.env['res.company'].browse(
                arg[2]).fiscal_company_id.id
            return ('company_id', operator, new_company_id)
        else:
            new_company_ids = self.env['res.company'].browse(
                arg[2]).mapped('fiscal_company_id').ids
            return ('company_id', operator, new_company_ids)
    else:
        return tuple(
            replace_company_id(self, arg[x]) for x in range(0, len(arg)))


def replace_company_id_dict(self, a):
    if a.get('company_id', False):
        a['company_id'] = self.pool.get("res.company").browse(
            a['company_id']).fiscal_company.id
    else:
        for key in a.keys():
            a[key] = replace_company_id(self, a[key])


def replace_company_id_list(self, a):
    return list(
        replace_company_id(self, a[x]) for x in range(0, len(a)))


def replace_company_id(self, a):
    if 'company_id' in str(a):
        if isinstance(a, tuple):
            return replace_company_id_tuple(self, a)
        elif isinstance(a, dict):
            return replace_company_id_dict(self, a)
        elif isinstance(a, list):
            return replace_company_id_list(self, a)
        else:
            return a
    else:
        return a


def switch_company_old_api(func):
    @functools.wraps(func)
    def wrapper(self, cr, uid, *args, **kwargs):
        rc_obj = self.pool.get("res.company")
        args2 = replace_company_id(self, cr, uid, args)
        context = kwargs.get('context', {})
        if context is None:
            context = {}
        c = context.copy()
        if context.get('company_id', False):
            try:
                c['company_id'] = rc_obj.browse(
                    cr, uid, context['company_id']).fiscal_company.id
            except:
                rc_id = rc_obj.search(
                    cr, uid, [('name', '=', context['company_id'])])
                try:
                    c['company_id'] = rc_obj.browse(
                        cr, uid, rc_id).fiscal_company.id
                except:
                    pass
            kwargs['context'] = c
        response = func(self, cr, uid, *args2, **kwargs)
        return response
    return wrapper

def switch_company(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        args2 = replace_company_id(self, args)
        response = func(self, *args2, **kwargs)
        return response
    return wrapper



def switch_company_period(func):
    @functools.wraps(func)
    def wrapper(self, cr, uid, *args, **kwargs):
        context = kwargs.get('context', {})
        if context is None:
            context = {}
        c = context.copy()
        if context.get('company_id', False):
            c['company_id'] = self.pool.get("res.company").browse(
                cr, uid, context['company_id']).fiscal_company.id
        else:
            c['company_id'] = self.pool.get('res.users').browse(
                cr, uid, uid, context=context).company_id.fiscal_company.id
        kwargs['context'] = c
        response = func(self, cr, uid, *args, **kwargs)
        return response
    return wrapper


def new_api_switch_company_period(func):
    """Decorator
        Replace the company_id of the context, by
        - the fiscal company of the company_id in the context;
        - OR by the fiscal company of the company_id of the current user;
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._context.get('company_id', False):
            company_id = self.env['res.company'].browse(
                self._context['company_id']).fiscal_company.id
        else:
            company_id = self.env.user.company_id.fiscal_company.id
        response = func(
            self.with_context(company_id=company_id), *args, **kwargs)
        return response
    return wrapper


def add_user_company(func):
    @functools.wraps(func)
    def wrapper(self, cr, uid, *args, **kwargs):
        context = kwargs.get('context', {})
        c = context.copy()
        if not context.get('company_id', False):
            c['company_id'] = self.pool.get('res.users').browse(
                cr, uid, uid, context=context).company_id.id
        kwargs['context'] = c
        response = func(self, cr, uid, *args, **kwargs)
        return response
    return wrapper
