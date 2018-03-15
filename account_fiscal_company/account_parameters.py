# coding: utf-8
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID


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
