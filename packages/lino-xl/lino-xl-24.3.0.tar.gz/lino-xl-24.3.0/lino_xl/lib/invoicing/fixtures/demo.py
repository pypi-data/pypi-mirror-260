# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino_xl.lib.invoicing.utils import invoicing_task, invoicing_rule
from lino.api import rt


def objects():

    yield invoicing_task("SLS")
    yield invoicing_rule("SLS", rt.models.sales.InvoiceItem)
    # yield invoicing_rule("SLS", rt.models.courses.Enrolment)
    # yield invoicing_rule("SLS", rt.models.courses.Course)
    # yield invoicing_rule("SLS", rt.models.rooms.Booking)
