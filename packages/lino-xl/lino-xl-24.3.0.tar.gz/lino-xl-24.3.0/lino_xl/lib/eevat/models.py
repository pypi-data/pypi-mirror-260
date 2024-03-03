# Copyright 2012-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _

from lino_xl.lib.vat.mixins import VatDeclaration

from .choicelists import DeclarationFields

DEMO_JOURNAL_NAME = "VAT"

# print("20170711a {}".format(DeclarationFields.get_list_items()))


class Declaration(VatDeclaration):

    fields_list = DeclarationFields

    class Meta:
        app_label = 'eevat'
        verbose_name = _("Estonian VAT declaration")
        verbose_name_plural = _("Estonian VAT declarations")


for fld in DeclarationFields.get_list_items():
    dd.inject_field('eevat.Declaration', fld.name, fld.get_model_field())

from .ui import *
