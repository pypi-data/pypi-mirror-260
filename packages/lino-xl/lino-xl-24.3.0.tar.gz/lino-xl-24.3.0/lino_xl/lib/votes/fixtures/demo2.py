# -*- coding: UTF-8 -*-
# Copyright 2016-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""We also to manually create demo votes in
:mod:`lino_noi.projects.care.lib.tickets.fixtures.demo`

"""

from lino.utils.cycler import Cycler
from lino.api import dd, rt


def objects():

    Vote = rt.models.votes.Vote
    VoteStates = rt.models.votes.VoteStates
    User = rt.models.users.User

    STATES = Cycler(VoteStates.objects())
    USERS = Cycler(User.objects.all())
    TICKETS = Cycler(dd.plugins.votes.votable_model.objects.all())
    if len(TICKETS):
        for i in range(20):
            USERS.pop()  # not every user votes
            obj = Vote(state=STATES.pop(),
                       user=USERS.pop(),
                       votable=TICKETS.pop())
            yield obj
            # 20210907
            # if obj.user != obj.votable.user:
            #     yield obj
