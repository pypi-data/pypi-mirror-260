# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.contrib.contenttypes.models import ContentType

from lino.api import rt


def invoicing_task(journal_ref, **kwargs):
    Journal = rt.models.ledger.Journal
    try:
        jnl = Journal.objects.get(ref=journal_ref)
    except Journal.DoesNotExist:
        raise Journal.DoesNotExist("No journal {} in {}".format(
            journal_ref, Journal.objects.all()))
    qs = rt.models.invoicing.Task.objects.filter(
        target_journal__ref=journal_ref)
    if qs.count() > 0:
        assert len(kwargs) == 0
        return qs.first()
    return rt.models.invoicing.Task(target_journal=jnl, **kwargs)


def invoicing_rule(journal_ref, ig, **kwargs):
    ct = ContentType.objects.get_for_model(ig)
    it = invoicing_task(journal_ref)
    return rt.models.invoicing.FollowUpRule(invoicing_task=it,
                                            invoice_generator=ct,
                                            **kwargs)
