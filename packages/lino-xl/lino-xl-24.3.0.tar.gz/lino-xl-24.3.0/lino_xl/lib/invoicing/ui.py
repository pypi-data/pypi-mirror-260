# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core import constants

from lino.modlib.users.mixins import My

from lino.api import dd, rt, _
from lino_xl.lib.ledger.roles import LedgerUser, LedgerStaff

# from .mixins import InvoicingAreas
from .actions import (ToggleSelection, StartInvoicing, StartInvoicingByArea,
                      StartInvoicingForPartner, StartInvoicingForOrder,
                      ExecutePlan, ExecuteItem)


class FollowUpRules(dd.Table):
    model = 'invoicing.FollowUpRule'
    # required_roles = dd.login_required(LedgerStaff)
    column_names = 'seqno invoicing_task invoice_generator source_journal *'


class RulesByTask(FollowUpRules):
    master_key = "invoicing_task"
    column_names = 'seqno invoice_generator source_journal *'


class TaskDetail(dd.DetailLayout):
    main = "general_tab cal_tab"

    general_tab = dd.Panel("""
    seqno target_journal
    invoice_generators
    invoicing.RulesByTask
    """,
                           label=_("General"))

    cal_tab = dd.Panel("""
    max_events every_unit every positions
    max_date_offset today_offset
    monday tuesday wednesday thursday friday saturday sunday
    log_level disabled status
    message
    """,
                       label=_("Calendar"))


class Tasks(dd.Table):
    model = 'invoicing.Task'
    column_names = 'seqno target_journal invoice_generators log_level disabled status *'
    required_roles = dd.login_required(LedgerStaff)
    detail_layout = 'invoicing.TaskDetail'


class SalesRules(dd.Table):
    model = 'invoicing.SalesRule'
    required_roles = dd.login_required(LedgerStaff)
    detail_layout = dd.DetailLayout("""
    partner
    invoice_recipient
    paper_type
    """,
                                    window_size=(40, 'auto'))


class PartnersByInvoiceRecipient(SalesRules):
    help_text = _("Show partners having this as invoice recipient.")
    details_of_master_template = _("%(master)s used as invoice recipient")
    button_text = "♚"  # 265A
    master_key = 'invoice_recipient'
    column_names = "partner partner__id partner__address_column *"
    window_size = (80, 20)


dd.inject_action(
    'contacts.Partner',
    show_invoice_partners=dd.ShowSlaveTable(PartnersByInvoiceRecipient))


class Tariffs(dd.Table):
    required_roles = dd.login_required(LedgerUser)
    model = "invoicing.Tariff"
    column_names = "designation number_of_events min_asset max_asset product *"
    order_by = ['designation']


class Plans(dd.Table):
    required_roles = dd.login_required(LedgerUser)
    model = "invoicing.Plan"
    detail_layout = """
    user invoicing_task #provision_product
    partner order today min_date max_date
    invoicing.ItemsByPlan
    """


class MyPlans(My, Plans):
    pass


class PlansByArea(Plans):
    master_key = 'invoicing_task'
    # detail_layout = """user source_journal partner
    # order today min_date max_date
    # invoicing.ItemsByPlan
    # """
    start_invoicing = StartInvoicingByArea()

    # @classmethod
    # def get_master_instance(self, ar, model, pk):
    #     if not pk:
    #         return None
    #     return InvoicingAreas.get_by_value(pk)


class AllPlans(Plans):
    required_roles = dd.login_required(LedgerStaff)


class Items(dd.Table):
    required_roles = dd.login_required(LedgerUser)
    model = "invoicing.Item"


class ItemsByPlan(Items):
    verbose_name_plural = _("Suggestions")
    master_key = 'plan'
    row_height = 2
    column_names = "selected partner preview number amount invoice_button *"
    display_mode = ((None, constants.DISPLAY_MODE_TABLE), )
    allow_create = False


class InvoicingsByGenerator(dd.Table):
    abstract = True
    required_roles = dd.login_required(LedgerUser)
    # model = dd.plugins.invoicing.item_model
    # model = 'ledger.Voucher'
    # model = Invoiceable
    label = _("Invoicings")
    master_key = 'invoiceable'
    editable = False
