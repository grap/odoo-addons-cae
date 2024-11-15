import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


_CORE_RULES = [
    "account_fiscal_year.account_fiscal_year_rule",  # account.fiscal.year
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
