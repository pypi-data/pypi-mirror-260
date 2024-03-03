# -*- coding: UTF-8 -*-
# Copyright 2023-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import logging
import sys
import traceback
import asyncio
from datetime import timedelta
from io import StringIO
from django.conf import settings
from django.utils import timezone
from asgiref.sync import sync_to_async

from lino.api import dd, rt, _
from lino.core.roles import SiteStaff
from lino import logger
from lino.mixins import Sequenced
from lino.modlib.checkdata.choicelists import Checker
from .choicelists import Procedures, LogLevels

# if dd.plugins.linod.use_channels:
#     from channels.db import database_sync_to_async

from .mixins import Runnable


class BackgroundTask(Runnable):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'BackgroundTask')
        app_label = 'linod'
        verbose_name = _("Background task")
        verbose_name_plural = _("Background tasks")

    procedure = Procedures.field(strict=False, unique=True, editable=False)

    def run_task(self, ar):
        return self.procedure.run(ar)

    def __str__(self):
        r = "{} #{} {}".format(self._meta.verbose_name, self.pk,
                               self.procedure.value)
        # if self.disabled:
        #     r += " ('disabled')"
        return r


class BackgroundTasks(dd.Table):
    # label = _("System tasks")
    model = 'linod.BackgroundTask'
    required_roles = dd.login_required(SiteStaff)
    column_names = "seqno procedure log_level disabled status *"
    detail_layout = """
    seqno procedure every every_unit
    log_level disabled status
    last_start_time last_end_time
    message
    """
    insert_layout = """
    procedure
    every every_unit
    """


class JobsChecker(Checker):
    """
    Checks for procedures that do not yet have a background task.
    """
    verbose_name = _("Check for missing background tasks")
    model = None

    def get_checkdata_problems(self, obj, fix=False):
        BackgroundTask = rt.models.linod.BackgroundTask

        for proc in Procedures.get_list_items():
            if BackgroundTask.objects.filter(procedure=proc).count() == 0:
                msg = _("No background task for {}").format(proc)
                yield (True, msg)
                if fix:
                    logger.debug("Create background task for %r", proc)
                    jr = BackgroundTask(procedure=proc, **proc.kwargs)
                    # every_unit=proc.every_unit, every=proc.every_value)
                    if jr.every_unit == "secondly":
                        jr.log_level = "WARNING"
                    jr.full_clean()
                    jr.save()


JobsChecker.activate()
