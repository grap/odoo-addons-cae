For the migration, take care of the tax.filtered occurences in Odoo and OCA modules.
There are a lot of ``filtered(lambda x: x.company_id == current_company)``
in Odoo. The module ``fiscal_company_account`` alter the behaviour of the function
``filtered`` of the ``account.tax`` module, to filter on the mother fiscal company.
However, the changes is imperfect, and multiple filters (company and not company filters)
will fail.

During migration, please run:
``rgrep "tax.*filtered.*company_id"``
