# -*- coding: UTF-8 -*-
# Copyright 2013-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from pathlib import Path
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from rstgen.utils import confirm
# from lino.management.commands.initdb import Command as BaseCommand
# from lino.management.commands.initdb import CommandError


class Command(BaseCommand):
    help = "Flush the database and load the default demo fixtures."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--noinput',
                            action='store_false',
                            dest='interactive',
                            default=True,
                            help='Do not prompt for input of any kind.'),
        parser.add_argument('--keepmedia',
                            action='store_true',
                            dest='keepmedia',
                            default=False,
                            help='Do not remove media files.'),

    def handle(self, *args, **options):
        if len(args) > 0:
            raise CommandError("This command takes no arguments (got %r)" %
                               args)

        if settings.SITE.readonly:
            settings.SITE.logger.info("No need to `prep` readonly site '%s'.",
                                      settings.SETTINGS_MODULE)
            return

        if settings.SITE.master_site:
            settings.SITE.logger.info("No need to `prep` slave site '%s'.",
                                      settings.SETTINGS_MODULE)
            return

        if settings.SITE.is_installed(
                'search') and settings.SITE.use_elasticsearch:
            call_command('createindexes', '-i')

        verbosity = options.get('verbosity')
        args = settings.SITE.demo_fixtures
        kwargs = dict()
        if isinstance(args, str):
            args = args.split()
        kwargs['interactive'] = options.get('interactive')
        kwargs['verbosity'] = verbosity
        if not options.pop('keepmedia'):
            kwargs['removemedia'] = True
        call_command('initdb', *args, **kwargs)

        settings.SITE.kernel.mark_virgin()
