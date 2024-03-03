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

from lino import logger
from lino.api import dd, rt, _
from lino.mixins import Sequenced
from lino.modlib.system.mixins import RecurrenceSet
from lino.modlib.system.choicelists import Recurrences
from .choicelists import LogLevels

# if dd.plugins.linod.use_channels:
#     from channels.db import database_sync_to_async


class RunNow(dd.Action):
    label = _("Run now")
    select_rows = True

    # icon_name = 'bell'
    # icon_name = 'lightning'

    def run_from_ui(self, ar, **kwargs):
        # print("20231102 RunNow", ar.selected_rows)
        for obj in ar.selected_rows:
            assert isinstance(obj, rt.models.linod.BackgroundTask)
            if True:  # dd.plugins.linod.use_channels:
                # Mark the task as to be executed asap by linod.
                obj.last_start_time = None
                obj.last_end_time = None
                obj.message = "{} requested to run this task at {}.".format(
                    ar.get_user(), dd.ftl(timezone.now()))
                obj.disabled = False
                obj.full_clean()
                obj.save()
            else:
                # Run the task myself (not in background).
                async_to_sync(obj.start_task)(ar)
        ar.set_response(refresh=True)


class Runnable(Sequenced, RecurrenceSet):

    class Meta:
        abstract = True

    log_level = LogLevels.field(default='INFO')
    disabled = dd.BooleanField(_("Disabled"), default=False)
    last_start_time = dd.DateTimeField(_("Started at"),
                                       null=True,
                                       editable=False)
    last_end_time = dd.DateTimeField(_("Ended at"), null=True, editable=False)
    message = dd.RichTextField(_("Logged messages"),
                               format='plain',
                               editable=False)

    run_now = RunNow()

    def full_clean(self, *args, **kwargs):
        if self.every_unit is None:
            self.every_unit = Recurrences.never
        super().full_clean(*args, **kwargs)

    @classmethod
    async def run_them_all(cls, ar):
        # Loops once over all tasks and runs those that are due to run. Returns
        # the suggested time for a next loop.

        # ar.debug("20231013 run_them_all()")
        now = timezone.now()
        next_time = now + timedelta(seconds=dd.plugins.linod.max_sleep_time)
        tasks = cls.objects.filter(disabled=False).order_by('seqno')
        async for self in tasks:
            # raise Warning("20231230")
            if self.last_end_time is None and self.last_start_time is not None:
                run_duration = now - self.last_start_time
                if run_duration > timedelta(hours=2):
                    msg = "Kill {} because it has been running more than 2 hours".format(
                        self)
                    ar.debug(msg)
                    self.last_end_time = now
                    self.message = msg
                    await sync_to_async(self.full_clean)()
                    # self.full_clean()
                    await self.asave()
                    # self.disabled = True
                else:
                    ar.debug("Skip running task %s", self)
                continue

            if self.last_end_time is not None:
                nst = self.get_next_suggested_date(self.last_end_time,
                                                   ar.logger)
                if nst > now:
                    ar.debug("Too early to start %s", self)
                    next_time = min(next_time, nst)
                    continue

            # ar.debug("Start %s", self)
            # print("20231021 1 gonna start", self)
            await self.start_task(ar)
            assert self.last_end_time is not None
            nst = self.get_next_suggested_date(self.last_end_time, ar.logger)
            next_time = min(next_time, nst)
        return next_time

    def is_running(self):
        return self.last_end_time is None and self.last_start_time is not None

    def run_task(self, ar):
        raise NotImplementedError()

    async def start_task(self, ar):
        # print("20231102 start_task", self)
        if self.is_running():
            raise Warning(_("{} is already running").format(self))
            # return
        ar.info("Start %s with logging level %s", self, self.log_level)
        self.last_start_time = timezone.now()
        # forget about any previous run:
        self.last_end_time = None
        self.message = ''
        # print("20231102 full_clean")
        await sync_to_async(self.full_clean)()
        # print("20231102 save")
        # await sync_to_async(self.save)()
        await self.asave()
        with ar.capture_logger(self.log_level.num_value) as out:
            # ar.info("Start %s using %s...", self, self.log_level)
            # print("20231021", ar.logger)
            try:
                await sync_to_async(self.run_task)(ar)
                # job.message = ar.response.get('info_message', '')
                ar.info("Successfully terminated %s", self)
                self.message = out.getvalue()
            except Exception as e:
                self.message = out.getvalue()
                self.message += '\n' + ''.join(traceback.format_exception(e))
                self.disabled = True
                ar.warning("Disabled %s after exception %s", self, e)
        self.last_end_time = timezone.now()
        self.message = "<pre>" + self.message + "</pre>"
        await sync_to_async(self.full_clean)()
        # await sync_to_async(self.save)()
        await self.asave()

    @dd.displayfield("Status")
    def status(self, ar=None):
        if self.is_running():
            return _("Running since {}").format(dd.ftl(self.last_start_time))
        if self.disabled:
            return _("Disabled")
        if self.last_start_time is None or self.last_end_time is None:
            if self.every_unit in (Recurrences.never, None):
                return _("Not scheduled")
            return _("Scheduled to run asap")
        next_time = self.get_next_suggested_date(self.last_end_time)
        if next_time is None:
            return _("Not scheduled")
        return _("Scheduled to run at {}").format(dd.ftl(next_time))

    @classmethod
    async def start_task_runner(cls, ar, max_count=None):
        # called from consumers.LinoConsumer.run_background_tasks()
        ar.logger.info("Start %s runner using %s...",
                       cls._meta.verbose_name_plural, ar.logger)
        # await sync_to_async(tasks.setup)()
        # print("20240109", ar.logger.handlers)
        count = 0
        while True:
            ar.logger.debug("Start next %s runner loop.",
                            cls._meta.verbose_name_plural)
            # asyncio.ensure_future
            next_dt = await cls.run_them_all(ar)
            # try:
            #     next_dt = await cls.run_them_all(ar)
            # except Exception as e:
            #     ar.logger.error(f"Stop background tasks runner after exception {e}.")
            #     return
            # next_dt = await sync_to_async(tasks.run)()
            # if not next_dt:
            #     break
            # if next_dt is True:
            #     continue
            count += 1
            if max_count is not None and count >= max_count:
                ar.logger.info("Stop after %s loops.", max_count)
                return
            if (to_sleep := (next_dt - timezone.now()).total_seconds()) <= 0:
                continue
            ar.logger.debug("Let %s runner sleep for %s seconds.",
                            cls._meta.verbose_name_plural, to_sleep)
            await asyncio.sleep(to_sleep)
