# coding: utf-8
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID


def propagate_properties_to_fiscal_childs(
        pool, cr, uid, ids, mother_company_id, model_name, property_name,
        property_value, context=None):
    """
        Propagate a property of objects of the same type for all fiscal
        child of mother company
        @param ids : ids of the objects ;
        @param mother_company_id : mother company into propagate property ;
        @param model_name : model name of the object ;
        @param property_name : name of the property ;
        @param property_value : value of the property ;
    """

    ip_obj = pool['ir.property']
    rc_obj = pool['res.company']
    imf_obj = pool['ir.model.fields']

    # Get fields information
    domain = [('model', '=', model_name), ('name', '=', property_name)]
    imf_id = imf_obj.search(cr, uid, domain, context=context)[0]
    imf = imf_obj.browse(cr, uid, imf_id, context=context)

    # Get company's information
    mother_rc = rc_obj.browse(cr, uid, mother_company_id, context=context)
    rc_ids = [x.id for x in mother_rc.fiscal_childs]

    for id in ids:
        # Delete all property
        domain = [
            ('res_id', '=', '%s,%s' % (model_name, id)),
            ('fields_id', '=', imf_id),
            ('company_id', 'in', rc_ids)]
        ip_ids = ip_obj.search(cr, SUPERUSER_ID, domain, context=context)
        ip_obj.unlink(cr, SUPERUSER_ID, ip_ids, context=context)

        # Create property for all fiscal childs
        if property_value:
            for rc_id in rc_ids:
                ip_vals = {
                    'name': property_name,
                    'res_id': '%s,%s' % (model_name, id),
                    'value': property_value,
                    'fields_id': imf.id,
                    'type': imf.ttype,
                    'company_id': rc_id,
                }
                ip_obj.create(cr, SUPERUSER_ID, ip_vals, context=context)


def propagate_properties_to_new_fiscal_child(
        pool, cr, uid, mother_company_id, child_company_id, model_name,
        property_name, context=None):
    """
        Propagate all properties of object of the same type for a new fiscal
        company
        @param mother_company_id : mother company into propagate property ;
        @param child_company_id : child company into propagate property ;
        @param model_name : model name of the object ;
        @param property_name : name of the property ;
    """
    ru_obj = pool['res.users']
    ip_obj = pool['ir.property']
    imf_obj = pool['ir.model.fields']

    # Get fields information
    domain = [('model', '=', model_name), ('name', '=', property_name)]
    imf_id = imf_obj.search(cr, uid, domain, context=context)[0]
    imf = imf_obj.browse(cr, uid, imf_id, context=context)

    # Get company's information
    ru_obj.write(
        cr, uid, [uid], {'company_id': mother_company_id}, context=context)
    my_obj = pool.get(model_name)
    my_ids = my_obj.search(cr, uid, [], context=context)
    my_values = my_obj.read(cr, uid, my_ids, [property_name], context=context)

    for item in my_values:
        # Create property for new fiscal child
        if item[property_name]:
            ip_vals = {
                'name': property_name,
                'res_id': '%s,%s' % (model_name, item['id']),
                'value': item[property_name][0],
                'fields_id': imf.id,
                'type': imf.ttype,
                'company_id': child_company_id,
            }
            ip_obj.create(cr, SUPERUSER_ID, ip_vals, context=context)
