# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api.ad import Plugin, _
from etgen.html import tostring


class Plugin(Plugin):

    verbose_name = _("Pages")
    ui_label = _("Pages")
    # needs_plugins = ['lino_xl.lib.topics', 'lino.modlib.office']
    # needs_plugins = ['lino.modlib.office', 'lino.modlib.publisher', 'lino_xl.lib.topics']
    needs_plugins = [
        'lino.modlib.linod', 'lino.modlib.publisher', 'lino_xl.lib.topics'
    ]
    menu_group = "publisher"

    def setup_main_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('pages.Pages')

    # def setup_explorer_menu(self, site, user_type, m):
    #     mg = self.get_menu_group()
    #     m = m.add_menu(mg.app_label, mg.verbose_name)
    #     m.add_action('pages.Nodes')
    #     m.add_action('pages.PageTypes')

    def get_requirements(self, site):
        yield "python-lorem"

    def post_site_startup(self, site):

        def toc(ar, text, cmdname, mentions, context):
            max_depth = 1
            if text:
                max_depth = int(text)
            # Node = site.models.pages.Node
            # return "X"
            this = context['self']

            # ctx = dict(width="{}%".format(int(100/len(photos))))
            # mentions.update(photos)
            def li(obj):
                #return "<li>{}</li>".format(obj.memo2html(ar, str(obj)))
                return "<li>{}</li>".format(tostring(ar.obj2html(obj)))

            html = ''.join([li(obj) for obj in this.children.all()])
            return "<ul class=\"toc\">{}</ul>".format(html)

        site.plugins.memo.parser.register_command('toc', toc)

        super().post_site_startup(site)
