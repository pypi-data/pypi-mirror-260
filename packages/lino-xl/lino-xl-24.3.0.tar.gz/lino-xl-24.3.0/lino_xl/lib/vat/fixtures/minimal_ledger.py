# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt
from django.conf import settings


def objects():
    ar = settings.SITE.login()
    rt.models.vat.VatColumnsChecker.update_unbound_problems(ar, fix=True)
    return []
