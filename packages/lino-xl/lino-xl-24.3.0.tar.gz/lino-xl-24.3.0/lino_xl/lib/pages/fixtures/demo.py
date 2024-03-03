# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lorem import get_paragraph
from django.utils import translation
from django.conf import settings
from lino.api import rt, dd, _
from lino.utils import Cycler

Page = rt.models.pages.Page
Node = rt.models.pages.Page
PublishingStates = rt.models.publisher.PublishingStates

welcome = _("""Welcome to our great website. We are proud to present
the best content about foo, bar and baz.

[toc]

""")

# BODIES = Cycler([lorem, short_lorem])
# blog_body = "[eval sar.show(settings.SITE.models.blogs.LatestEntries)]"
# blog_body = "[show blogs.LatestEntries]"
PARA = "<p>" + get_paragraph(count=4, sep="</p><p>") + "</p>"
photos_children = []


def add(*args):
    photos_children.append(args)


add(
    _("Default formatting"), """
<p><tt>\\[upload 6]</tt> inserts the image inline, without any text wrapping.
The following image has been inserted using a <tt>\\[upload 6]</tt> without any surrounding text inside a centered paragraph.
<p align=\"center\">[upload 6]</p>
""" + get_paragraph() + PARA, Page, [])

add(
    _("Thumbnail"), """
<p>[upload 6 thumb|] <tt>\\[upload 6 thumb|]</tt> makes the image float right with a height of 10em. """
    + get_paragraph() + PARA, Page, [])
add(
    _("Thumbnail left"), """
<p>[upload 6 thumb|left|]  <tt>\\[upload 6 thumb|left|]</tt> makes the image
float left instead of right.
""" + get_paragraph() + PARA, Page, [])
add(_("Tiny thumbnail"), """<p>[upload 6 tiny|] """ + get_paragraph() + PARA,
    Page, [])
add(_("Tiny thumbnail left"),
    """<p>[upload 6 tiny|left|] """ + get_paragraph() + PARA, Page, [])
# add(_("trio"), PARA + "<p align=\"center\">[upload 11 trio|] [upload 12 trio|] [upload 8 trio|]</p>"+PARA, None, [])
# add(_("duo"), PARA + "<p align=\"center\">[upload 11 duo|] [upload 6 duo|]</p>"+PARA, None, [])
# add(_("solo"), PARA + "<p align=\"center\">[upload 11 solo|]</p>"+PARA, None, [])
add(
    _("Wide"), """
<tt>\\[upload 11 wide|]</tt> inserts the image in a standalone paragraph and
using the whole available text width.
""" + "[upload 11 wide|]" + PARA, Page, [])
# add("[photorow]", PARA + "[photorow 5 6 7 8]"+PARA, None, [])
add(
    _("Gallery"),
    "<p>The <tt>\[gallery ]</tt> command accepts any number of primary keys and inserts a centered paragraph with these pictures.</p>"
    + "[gallery 5 6 7 8 9 10 11 13 14]" + PARA, Page, [])

simple_nodes = """
This page has a number of sections and subsections defined as simple nodes, i.e.
which don't have any HTML page on its own, which means
their headings are not clickable.
""" + PARA

home_children = [(_("Services"), simple_nodes, Page, [
    (_("Washing"), None, Node, []),
    (_("Drying"), None, Node, [(_("Air drying"), None, Node, []),
                               (_("Machine drying"), None, Node,
                                [(_("Drying foos"), None, Node, []),
                                 (_("Drying bars"), None, Node, []),
                                 (_("Drying bazes"), None, Node, [])])]),
    (_("Ironing"), None, Node, []),
]), (_("Prices"), None, Page, []), (_("Photos"), None, Page, photos_children),
                 (_("About us"), None, Page, [
                     (_("Team"), None, Page, []),
                     (_("History"), None, Page, []),
                     (_("Contact"), None, Page, []),
                     (_("Terms & conditions"), None, Page, []),
                 ])]

# if dd.is_installed("blogs"):
#     home_children.append((_("Blog"), blog_body, "blogs.LatestEntries", []))
# if dd.is_installed("comments"):
#     home_children.append((_("Recent comments"), "", "comments.RecentComments", []))

site_pages = [(_("Home"), welcome, Page, home_children)]

# from pprint import pprint
# pprint(pages)


def objects():
    # Translation = rt.models.pages.Translation
    # for lc in settings.SITE.LANGUAGE_CHOICES:
    #     language = lc[0]
    #     kwargs = dict(language=language, ref='index')
    #     with translation.override(language):

    parent_nodes = []
    for lng in settings.SITE.languages:
        counter = {None: 0}
        # count = 0
        with translation.override(lng.django_code):

            def make_pages(pages, parent=None):
                # trans_parent = None
                for title, body, model, children in pages:
                    if model is None:
                        raise Exception(str(title))
                    kwargs = dict(title=title)
                    # kwargs = dd.str2kw("title", title, **kwargs)
                    # if filler:
                    #     kwargs.update(filler=filler)
                    # kwargs.update(page_type=rt.models.pages.PageTypes.pages)
                    if body is None:
                        kwargs.update(body=get_paragraph())
                    else:
                        kwargs.update(body=body)
                    if model is Page:
                        if parent is None:
                            kwargs.update(ref='index')
                        if lng.suffix:
                            kwargs.update(
                                translated_from=parent_nodes[counter[None]])
                        kwargs.update(language=lng.django_code)
                        if dd.is_installed("publisher"):
                            kwargs.update(publishing_state='published')
                    obj = model(parent=parent, **kwargs)
                    yield obj
                    if not lng.suffix:
                        parent_nodes.append(obj)
                    # if lng.suffix:
                    #     kwargs.update(translated_from=parent_nodes[counter[None]])
                    #     yield Translation(parent=parent_nodes[counter[None]],
                    #         child=obj, language=lng.django_code)
                    #     # assert trans_parent is not None
                    #     # yield Translation(parent=trans_parent,
                    #     #     child=obj, language=lng.django_code)
                    # else:
                    #     parent_nodes.append(obj)
                    # trans_parent = obj
                    # ref = None
                    counter[None] += 1
                    # print("20230324", title, kwargs)
                    # count += 1
                    yield make_pages(children, obj)

            yield make_pages(site_pages)
