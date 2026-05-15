import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


_CORE_RULES = [
    "base.res_company_rule_employee",  # res.company
    "base.res_partner_rule",  # res.partner
]


def post_init_hook(cr, registry):
    _toggle_standard_rules(cr, False)


def uninstall_hook(cr, registry):
    _toggle_standard_rules(cr, True)


def _toggle_standard_rules(cr, enabled):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for xml_id in _CORE_RULES:
        rule = env.ref(xml_id)
        rule.active = enabled
