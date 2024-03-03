# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger

import os
import io
from copy import copy

from django.conf import settings
from django.db import models
from django.utils import translation
from etgen.html import tostring
from django.utils.text import format_lazy

try:
    from django.template import TemplateDoesNotExist
except ImportError:
    from django.template.loader import TemplateDoesNotExist

from django.template.loader import select_template

from lino.core.choicelists import ChoiceList, Choice
from lino.utils.media import MediaFile
from lino.api import dd, rt, _

# class PageType(Choice):
#
#     nodes_table = 'pages.Node'
#
#     def __init__(self, nodes_table, names=None):
#         self.nodes_table = nodes_table
#         super().__init__(str(nodes_table), str(nodes_table), names)
#
# class PageTypes(ChoiceList):
#     # verbose_name = _("Build method")
#     verbose_name = _("Page type")
#     verbose_name_plural = _("Page types")
#     item_class = PageType
#     max_length = 50
#     column_names = "value name text nodes_table *"
#
#     @dd.virtualfield(models.CharField(_("Nodes table")))
#     def nodes_table(cls, choice, ar):
#         return choice.nodes_table


class PageFiller(Choice):
    data_view = None

    def __init__(self, data_view, *args, **kwargs):
        self.data_view = data_view
        super().__init__(str(data_view), *args, **kwargs)

    def get_dynamic_story(self, ar, obj, **kwargs):
        txt = ''
        dv = self.data_view
        sar = dv.request(parent=ar, limit=dv.preview_limit)
        print("20231028", dv, list(sar))
        # print("20230409", ar.renderer)
        # rv += "20230325 [show {}]".format(dv)
        for e in sar.renderer.table2story(sar, **kwargs):
            txt += tostring(e)
        return txt

    def get_dynamic_paragraph(self, ar, obj, **kwargs):
        dv = self.data_view
        # sar = dv.request(parent=ar, limit=dv.preview_limit)
        sar = dv.request(parent=ar)
        return " / ".join([sar.obj2htmls(row) for row in sar])


class PageFillers(ChoiceList):
    verbose_name = _("Page filler")
    verbose_name_plural = _("Page fillers")
    item_class = PageFiller
    max_length = 50
    column_names = "value name text data_view *"

    @dd.virtualfield(models.CharField(_("Data view")))
    def data_view(cls, choice, ar):
        return choice.data_view


# class LinkType(dd.Choice):
#
#     def __init__(self, value, text, names, **kw):
#         super().__init__(value, text, names, **kw)
#
#
# class LinkTypes(dd.ChoiceList):
#     required_roles = dd.login_required(dd.SiteStaff)
#     verbose_name = _("Node link type")
#     verbose_name_plural = _("Node link types")
#     item_class = LinkType
#
# add = LinkTypes.add_item
# add('010', _("Translation"), 'translation')
