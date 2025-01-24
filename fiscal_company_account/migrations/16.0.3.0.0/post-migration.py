# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    IrProperty = env["ir.property"]
    mother_companies = env["res.company"].search(
        [("fiscal_type", "=", "fiscal_mother")]
    )

    todo_list = [
        ("property_account_receivable_id", "res.partner"),
        ("property_account_payable_id", "res.partner"),
    ]

    for field, model in todo_list:
        for mother_company in mother_companies:
            value = IrProperty.with_company(mother_company)._get(field, model)
            if value:
                for company in mother_company.child_ids:
                    _logger.info(
                        f"Company {company.code}-{company.name}. Model {model}."
                        " Field: {field}. New default value: {value}"
                    )
                    IrProperty._set_default(field, model, value, company=company)
