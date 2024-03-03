# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# DEPRECATED. This whole module can probably go away because
# InterestsByController has an insert button.

from lino.core.gfks import gfk2lookup
from lino.utils.instantiator import create_row
from lino.api import dd, rt, _
from .roles import TopicsUser

if dd.is_installed("topics"):

    class AddInterestField(dd.VirtualField):
        """An editable virtual field used for adding an interest to the
    object.

    """
        editable = True

        def __init__(self):
            return_type = dd.ForeignKey('topics.Topic',
                                        verbose_name=_("Add interest"),
                                        blank=True,
                                        null=True)
            dd.VirtualField.__init__(self, return_type, None)

        def set_value_in_object(self, request, obj, value):
            # dd.logger.info("20170508 set_value_in_object(%s, %s)", obj, value)
            # if value is None:
            #     raise Exception("20170508")
            if value is not None:
                Interest = rt.models.topics.Interest
                if Interest.objects.filter(**gfk2lookup(
                        Interest.owner, obj, topic=value)).count() == 0:
                    try:
                        create_row(Interest, topic=value, owner=obj)
                    except Exception as e:
                        dd.logger.warning("20170508 ignoring %s", e)
            return obj

        def value_from_object(self, obj, ar):
            return None

else:

    AddInterestField = dd.DummyField


class Interesting(dd.Model):

    class Meta:
        abstract = True
        app_label = 'topics'

    add_interest = AddInterestField()
