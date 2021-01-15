
from odoo import api, SUPERUSER_ID


def post_install_set_fiscal_company(cr, registry):
    """Initialize correctly fiscal_company_id for
    existing companies (that are normal, by default)
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        companies = env["res.company"].with_context(
            active_test=False).search([("fiscal_type", "!=", "fiscal_child")])
        for company in companies:
            company.fiscal_company_id = company.id
