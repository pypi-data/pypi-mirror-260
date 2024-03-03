# -*- coding: UTF-8 -*-
# Copyright 2023-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import logging
from typing import Callable
from lino.api import dd, _
from lino.core.roles import SiteStaff


class Procedure(dd.Choice):
    func: Callable
    kwargs: dict

    def __init__(self, func, **kwargs):
        name = func.__name__
        super().__init__(name, name, name)
        self.func = func
        self.kwargs = kwargs

    def run(self, ar):
        return self.func(ar)

    def __repr__(self):
        return f"Procedures.{self.value}"


class Procedures(dd.ChoiceList):
    verbose_name = _("Background procedure")
    verbose_name_plural = _("Background procedures")
    max_length = 100
    item_class = Procedure
    column_names = "value name text kwargs"
    required_roles = dd.login_required(SiteStaff)

    @dd.virtualfield(dd.CharField(_("Suggested recurrency")))
    def kwargs(cls, choice, ar):
        return ", ".join(
            ["{}={}".format(*i) for i in sorted(choice.kwargs.items())])


class LogLevel(dd.Choice):
    num_value = logging.NOTSET

    def __init__(self, name):
        self.num_value = getattr(logging, name)
        super().__init__(name, name, name)


class LogLevels(dd.ChoiceList):
    verbose_name = _("Logging level")
    verbose_name_plural = _("Logging levels")
    item_class = LogLevel
    column_names = "value text num_value"

    @dd.virtualfield(dd.IntegerField(_("Numeric value")))
    def num_value(cls, choice, ar):
        return choice.num_value


LogLevel.set_widget_options('num_value', hide_sum=True)

add = LogLevels.add_item
add('DEBUG')
add('INFO')
add('WARNING')
add('ERROR')
add('CRITICAL')
