# -*- coding: UTF-8 -*-
# Copyright 2022-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# import time
import os
import asyncio

from django.conf import settings
from django.core.management import BaseCommand, call_command
from lino.api import dd, rt

if dd.plugins.linod.use_channels:

    import threading
    from channels.layers import get_channel_layer
    from lino.modlib.linod.utils import CHANNEL_NAME


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            help=
            "Force starts the runworker process even if a log_socket_file exists."
            " Use only in production server.",
            action="store_true",
            default=False)
        # parser.add_argument("--skip-system-tasks",
        #                     help="Skips the system tasks coroutine",
        #                     action="store_true",
        #                     default=False)

    def handle(self, *args, **options):

        if not dd.plugins.linod.use_channels:
            ar = rt.login()
            ar.logger.debug("Lino daemon running without channels")
            asyncio.run(rt.models.linod.BackgroundTask.start_task_runner(ar))
            return

        log_sock_path = settings.SITE.log_sock_path

        if log_sock_path and log_sock_path.exists():
            if options.get('force'):
                log_sock_path.unlink()
            else:
                raise Exception(
                    f"log socket already exists: {log_sock_path}\n"
                    "It's probable that a worker process is already running. "
                    "Try: 'ps awx | grep linod' OR 'sudo supervisorctl status | grep worker'\n"
                    "Or the last instance of the worker process did not finish properly. "
                    "In that case remove the file and run this command again.")

        # worker_sock_path.unlink(True)
        # log_sock_path.unlink(True)

        def start_channels():
            try:
                asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                # loop.set_debug(True)
                asyncio.set_event_loop(loop)
            call_command('runworker', CHANNEL_NAME)

        worker_thread = threading.Thread(target=start_channels)
        worker_thread.start()

        async def initiate_linod():
            layer = get_channel_layer()
            # if log_sock_path is not None:
            await layer.send(CHANNEL_NAME, {'type': 'log.server'})
            # await asyncio.sleep(1)
            await layer.send(CHANNEL_NAME, {'type': 'run.background.tasks'})

        # print("20240108 a")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(initiate_linod())
        # print("20240108 c")

        try:
            worker_thread.join()
        except KeyboardInterrupt:
            print("Finishing thread...")
            worker_thread.join(0)
