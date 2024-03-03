# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from etgen.html import E
from lino.api import dd, rt, _
from django.db import models

# from lino.core.utils import comma
from lino.core.gfks import gfk2lookup
from lino.mixins import BabelNamed
from lino.mixins.ref import StructuredReferrable
from lino.utils import join_elems
from lino.utils.instantiator import create_row
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.publisher.mixins import Publishable
from lino.core import constants
from .roles import TopicsUser

# class TopicGroup(BabelNamed):

#     class Meta:
#         app_label = 'topics'
#         verbose_name = _("Topic group")
#         verbose_name_plural = _("Topic groups")
#         abstract = dd.is_abstract_model(__name__, 'TopicGroup')

#     description = models.TextField(_("Description"), blank=True)

# class TopicGroups(dd.Table):
#     model = 'topics.TopicGroup'
#     required_roles = dd.login_required(dd.SiteStaff)
#     order_by = ["id"]
#     # detail_layout = """
#     # id name
#     # description
#     # TopicsByGroup
#     # """


#
class Interest(Controllable):

    class Meta:
        app_label = 'topics'
        verbose_name = _("Interest")
        verbose_name_plural = _('Interests')

    allow_cascaded_delete = ["partner"]

    topic = dd.ForeignKey('topics.Topic', related_name='interests_by_topic')
    remark = dd.RichTextField(_("Remark"), blank=True, format="plain")
    partner = dd.ForeignKey(dd.plugins.topics.partner_model,
                            related_name='interests_by_partner',
                            blank=True,
                            null=True)


# dd.update_field(Interest, 'user', verbose_name=_("User"))


#
class Topic(StructuredReferrable, BabelNamed, Publishable):

    ref_max_length = 5

    class Meta:
        app_label = 'topics'
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        abstract = dd.is_abstract_model(__name__, 'Topic')

    description_text = dd.BabelTextField(verbose_name=_("Long description"),
                                         blank=True,
                                         null=True)


class Topics(dd.Table):
    required_roles = dd.login_required(TopicsUser)
    model = 'topics.Topic'
    order_by = ["ref"]
    column_names = "ref name *"

    insert_layout = """
    ref
    name
    """

    detail_layout = """
    id ref name #topic_group
    description_text
    topics.InterestsByTopic
    """


class AllTopics(Topics):
    required_roles = dd.login_required(dd.SiteStaff)


# class TopicsByGroup(Topics):
#     master_key = 'topic_group'
#     required_roles = dd.login_required(dd.SiteStaff)


class Interests(dd.Table):
    required_roles = dd.login_required(TopicsUser)
    model = 'topics.Interest'
    column_names = "partner topic *"
    detail_layout = dd.DetailLayout("""
    partner
    topic owner
    remark
    """,
                                    window_size=(60, 15))


class AllInterests(Interests):
    required_roles = dd.login_required(dd.SiteStaff)


class InterestsByPartner(Interests):
    master_key = 'partner'
    order_by = ["topic"]
    column_names = 'topic *'
    display_mode = ((None, constants.DISPLAY_MODE_SUMMARY), )
    stay_in_grid = True

    insert_layout = dd.InsertLayout("""
    topic
    remark
    """,
                                    window_size=(60, 10))

    # summary_sep = comma

    @classmethod
    def row_as_summary(cls, ar, obj, **kwargs):
        if ar is None:
            return str(obj.topic)
        else:
            return ar.obj2htmls(obj, str(obj.topic))


class InterestsByController(Interests):
    master_key = 'owner'
    order_by = ["topic"]
    column_names = 'topic *'
    stay_in_grid = True
    display_mode = ((None, constants.DISPLAY_MODE_SUMMARY), )
    insert_layout = dd.InsertLayout("""
    topic partner
    remark
    """,
                                    window_size=(60, 10))

    # summary_sep = comma

    @classmethod
    def row_as_summary(cls, ar, obj, **kwargs):
        if ar is None:
            return str(obj.topic)
        else:
            return ar.obj2html(obj, str(obj.topic))


class InterestsByTopic(Interests):
    master_key = 'topic'
    order_by = ["id"]
    column_names = 'partner owner *'
