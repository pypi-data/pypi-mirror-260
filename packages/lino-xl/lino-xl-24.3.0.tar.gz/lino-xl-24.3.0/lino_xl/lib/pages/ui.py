# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from html import escape
from django.db import models
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import translation
from django.utils.translation import pgettext_lazy
# from django.utils.translation import get_language
from django.utils.html import mark_safe

from lino.api import dd, rt, _
from etgen.html import E, tostring_pretty
from lino.core import constants
# from lino.core.renderer import add_user_language

from lino.utils.mldbc.fields import LanguageField
from lino import mixins
from lino.mixins import Hierarchical, Sequenced, Referrable
from lino.modlib.office.roles import OfficeUser
from lino.modlib.publisher.mixins import Publishable
# from lino.modlib.publisher.choicelists import PublisherViews
from lino.modlib.comments.mixins import Commentable
from lino.modlib.memo.mixins import Previewable
# from .utils import render_node
# from .choicelists import PageFillers
# from .choicelists import PageTypes, PageFillers

# class NodeDetail(dd.DetailLayout):
#     main = "first_panel general more"
#
#     first_panel = dd.Panel("""
#     treeview_panel:20 preview:60
#     """, label=_("Preview"))
#
#     general = dd.Panel("""
#     content_panel:60 right_panel:20
#     """, label=_("General"), required_roles=dd.login_required(OfficeUser))
#
#     more = dd.Panel("""
#     # topics.InterestsByController:20 add_interest
#     comments.CommentsByRFC:20
#     """, label=_("More"), required_roles=dd.login_required(OfficeUser))
#
#     content_panel = """
#     title id
#     body
#     pages.PagesByParent
#     """
#
#     right_panel = """
#     parent seqno
#     child_node_depth
#     page_type
#     filler
#     """
#
#
# class Nodes(dd.Table):
#     model = 'pages.Node'
#     column_names = "title page_type id *"
#     order_by = ["id"]
#     detail_layout = 'pages.NodeDetail'
#     insert_layout = """
#     title
#     page_type filler
#     """
#     display_mode = ((None, constants.DISPLAY_MODE_STORY),)
#
#

# class Translations(dd.Table):
#     model = 'pages.Translation'
#
# class TranslationsByParent(Translations):
#     master_key = 'parent'
#     label = _("Translated to...")
#
# class TranslationsByChild(Translations):
#     master_key = 'child'
#     label = _("Translated from...")


class PageDetail(dd.DetailLayout):
    main = "first_panel general more"

    first_panel = dd.Panel("""
    treeview_panel:20 preview:60
    """,
                           label=_("Preview"))

    general = dd.Panel("""
    content_panel:60 right_panel:20
    """,
                       label=_("General"),
                       required_roles=dd.login_required(OfficeUser))

    more = dd.Panel("""
    topics.InterestsByController:20 comments.CommentsByRFC:60
    """,
                    label=_("Discussion"),
                    required_roles=dd.login_required(OfficeUser))

    content_panel = """
    title id
    body
    pages.PagesByParent
    """

    # right_panel = """
    # parent seqno
    # child_node_depth
    # page_type
    # filler
    # """

    right_panel = """
    ref
    parent seqno
    child_node_depth
    #page_type filler
    language
    pages.TranslationsByPage
    """


class Pages(dd.Table):
    model = 'pages.Page'
    column_names = "ref title #page_type id *"
    detail_layout = 'pages.PageDetail'
    insert_layout = """
    title
    ref
    #page_type filler
    """
    display_mode = ((None, constants.DISPLAY_MODE_STORY), )


class PagesByParent(Pages):
    master_key = 'parent'
    label = _("Children")
    #~ column_names = "title user *"
    order_by = ["seqno"]
    column_names = "seqno title *"
    display_mode = ((None, constants.DISPLAY_MODE_LIST), )


# PublisherViews.add_item_lazy("p", Pages)
# PublisherViews.add_item_lazy("n", Nodes)

# PageTypes.add_item(Pages, 'pages')


class TranslationsByPage(Pages):
    master_key = 'translated_from'
    label = _("Translations")
    column_names = "ref title language id *"
    display_mode = ((None, constants.DISPLAY_MODE_SUMMARY), )

    @classmethod
    def row_as_summary(cls, ar, obj, **kwargs):
        return ("({}) ".format(obj.language)) + obj.as_summary_row(
            ar, **kwargs)
