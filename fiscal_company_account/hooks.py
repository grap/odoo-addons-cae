import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


_CORE_RULES = [
    "account.account_comp_rule",  # account.account
    "account.account_fiscal_position_comp_rule",  # account.fiscal.position
    "account.journal_comp_rule",  # account.journal
    "account.account_root_comp_rule",  # account.root
    "account.tax_comp_rule",  # account.tax
    "account.tax_rep_comp_rule",  # account.tax.repartition.line
]


def post_init_hook(cr, registry):
    _toggle_standard_rules(cr, False)


def uninstall_hook(cr, registry):
    _toggle_standard_rules(cr, True)


def _toggle_standard_rules(cr, enabled):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for xml_id in _CORE_RULES:
        rule = env.ref(xml_id)
        if rule.active != enabled:
            _logger.info(f"Default rule {xml_id}. Active set to {enabled}.")
            rule.active = enabled
