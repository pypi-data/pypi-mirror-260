# -*- coding: UTF-8 -*-
# Copyright 2009-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# doctest lino/core/site.py
"""
Defines the :class:`Site` class.
See :doc:`/dev/site` and :doc:`/dev/plugins` and :doc:`/dev/languages`.

"""

import os
import sys
from os.path import normpath, dirname, join, isdir, relpath, exists, abspath
import inspect
import datetime
import warnings
import collections
import locale
import logging
from logging.handlers import SocketHandler
import time
try:
    from bleach.sanitizer import ALLOWED_ATTRIBUTES
except ImportError:
    ALLOWED_ATTRIBUTES = dict()

ASYNC_LOGGING = False
# This is to fix the issue that the "started" and "ended" messages are not logged.
# But setting this to True causes #4986 (Unable to configure handler 'mail_admins')
# because since 20230529 we called logging..config.dictConfig() during
# lino.core.site.Site.setup_logging(). The Django default logger config, when
# activated, accesses settings.DEFAULT_EXCEPTION_REPORTER, which fails at this
# moment because the settings aren't yet loaded.

# from unipath import Path
from pathlib import Path
from importlib import import_module, reload
from importlib.util import find_spec

from lino import logger
from lino.utils import AttrDict, date_offset, i2d, buildurl
import rstgen

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.db.utils import DatabaseError
from django.utils import translation

has_socialauth = find_spec('social_django') is not None
has_elasticsearch = find_spec('elasticsearch_django') is not None
has_haystack = find_spec('haystack') is not None

from rstgen.confparser import ConfigParser
from lino.core.plugin import Plugin
from lino.core import constants

from lino import assert_django_code, DJANGO_DEFAULT_LANGUAGE
from etgen.html import E, join_elems, tostring
from lino.core.utils import get_models, is_logserver

# from lino.utils.html2text import html2text
# from html2text import html2text
from lino.core.exceptions import ChangedAPI
# from .roles import SiteUser
# from lino.core.features import FEATURES_HOOKS#, LINO_FEATURES

import re

# _INSTANCES = []


class LinoSocketHandler(SocketHandler):
    # see: https://code.djangoproject.com/ticket/29186
    def emit(self, record):
        # print("20231019 LinoSocketHandler.emit()", record)
        if hasattr(record, 'request'):
            record.request = "Removed by LinoSocketHandler"
        return super().emit(record)
        # try:
        #     return super().emit(record)
        # except Exception as e:
        #     logging.warning(f"Non-picklable LogRecord: {record}\n" + dd.read_exception(sys.exc_info()))


def classdir(cl):
    # return the full absolute resolved path name of the directory containing
    # the file that defines class cl.
    return os.path.realpath(dirname(inspect.getfile(cl)))


LanguageInfo = collections.namedtuple(
    'LanguageInfo', ('django_code', 'name', 'index', 'suffix'))
":noindex:"


def to_locale(language):
    """
    Simplified copy of `django.utils.translation.to_locale`, but we
    need it while the `settings` module is being loaded, i.e. we
    cannot yet import django.utils.translation.  Also we don't need
    the to_lower argument.
    """
    p = language.find('-')
    if p >= 0:
        # Get correct locale for sr-latn
        if len(language[p + 1:]) > 2:
            return language[:p].lower() + '_' \
                + language[p + 1].upper() + language[p + 2:].lower()
        return language[:p].lower() + '_' + language[p + 1:].upper()
    else:
        return language.lower()


def class2str(cl):
    return cl.__module__ + '.' + cl.__name__


gettext_noop = lambda s: s

PLUGIN_CONFIGS = {}

# def configure_plugin(app_label, **kwargs):
#     """
#     Set one or several configuration settings of the given plugin
#     *before* the :setting:`SITE` has been instantiated.
#
#     This might get deprecated some day. Consider using the
#     :meth:`Site.get_plugin_configs` method instead.
#
#     See :doc:`/dev/plugins`.
#     """
#     # if PLUGIN_CONFIGS is None:
#     #     raise ImproperlyConfigured(
#     #         "Tried to call configure_plugin after Site instantiation")
#     cfg = PLUGIN_CONFIGS.setdefault(app_label, {})
#     cfg.update(kwargs)


# from django.db.models.fields import NOT_PROVIDED
class NOT_PROVIDED(object):
    pass


# def is_socket_alive(sock_file: Path) -> bool:
#     if not sock_file.exists():
#         return False
#     return True
#     # # Inspired by https://stackoverflow.com/questions/48024720/python-how-to-check-if-socket-is-still-connected
#     # try:
#     #     # this will try to read bytes without blocking and also without removing them from buffer (peek only)
#     #     data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
#     #     if len(data) == 0:
#     #         return True
#     # except BlockingIOError:
#     #     return False  # socket is open and reading from it would block
#     # except ConnectionResetError:
#     #     return True  # socket was closed for some other reason
#     # except Exception as e:
#     #     logger.exception("unexpected exception when checking if a socket is closed")
#     #     return False
#     # return False


class Site(object):
    """
    The base class for a Lino application.  This class is designed to
    be overridden by both application developers and local site
    administrators.  Your :setting:`SITE` setting is expected to
    contain an instance of a subclass of this.

    .. attribute:: plugins

        An :class:`AttrDict <atelier.utils.AttrDict>` with one entry
        for each installed plugin, mapping the `app_label` of every
        plugin to the corresponding :class:`lino.core.plugin.Plugin`
        instance.

        This attribute is automatically filled by Lino and available as
        :attr:`dd.plugins <lino.api.dd>` already before Django starts to
        import :xfile:`models.py` modules.

    .. attribute:: modules

        Old name for :attr:`models`.  Deprecated.

    .. attribute:: models

        An :class:`AttrDict <atelier.utils.AttrDict>` which maps every
        installed `app_label` to the corresponding :xfile:`models.py`
        module object.

        This is also available as the shortcut :attr:`rt.models
        <lino.api.rt.models>`.

        See :doc:`/dev/plugins`

    .. attribute:: beid_protocol

        Until 20180926 this was a string like e.g. 'beid' in order to
        use a custom protocol for reading eid cards.  Now it is
        deprecated.  Use :attr:`lino_xl.lib.beid.Plugin.urlhandler_prefix`
        instead.

    """

    KB = 2**10
    MB = 2**20

    quantity_max_length = 6
    """The default value for `max_length` of quantity fields."""

    upload_to_tpl = 'uploads/%Y/%m'
    """The value to use as
    `upload_to
    <https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.FileField.upload_to>`__
    for the :attr:`Upload.file` field.
    """

    auto_fit_column_widths = True
    """
    The default value for the :attr:`auto_fit_column_widths
    <lino.core.tables.AbstractTable.auto_fit_column_widths>` of tables
    in this application.
    """

    # locale = 'en_GB.utf-8'
    site_locale = None
    """
    The `locale <https://docs.python.org/3/library/locale.html>`__ to
    use for certain localized things on this site.

    Used by :meth:`format_currency`.

    This should be a string of type '<language>_<country>.<encoding>',
    and it must have been generated previously.  For example::

        sudo locale-gen de_BE.utf8
    """

    confdirs = None
    """
    Pointer to the config directories registry.
    See :ref:`config_dirs` and :mod:`lino.utils.config`.
    Lino sets this attribute during site startup.
    """

    kernel = None
    """
    This attribute is available only after :meth:`startup`.
    See :mod:`lino.core.kernel`.

    """

    # ui = None
    # """
    # Deprecated alias for :attr:`kernel`.

    # """

    readonly = False
    """Setting this to `True` turns this site in a readonly site.  This
    means that :setting:`DATABASES` must point to the
    :setting:`DATABASES` of some other (non-readonly) site, and that
    :manage:`initdb` will do nothing.

    """

    _history_aware_logging = False
    """Whether to log a message :message:`Started %s (using %s) --> PID
    %s` at process startup (and a message :message:`Done PID %s` at
    termination).

    This kind of messages are usually disturbing for development and testing,
    but they are interesting e.g. when a system administrator wants to know
    which processes have been running on a given production site.

    This is automatically set to `True` when a logger directory (:xfile:`log`)
    exists in the project directory.

    See also :ref:`host.logging`.

    """

    the_demo_date = None
    """A hard-coded constant date to be used as reference by :meth:`today`
    and :meth:`demo_date`.

    Many demo projects have this set because certain tests rely on a constant
    reference date.

    This is either `None` or a :class:`datetime.date` object, If it is an
    :class:`int` or a :class:`str`, Lino will convert it during startup to a
    :class:`datetime.date` using :func:`rstgen.utils.i2d`.

    """

    hoster_status_url = "http://bugs.saffre-rumma.net/"
    """This is mentioned in :xfile:`500.html`.
    """

    title = None
    verbose_name = "yet another Lino application"

    description = None
    """
    A multi-line plain text description of up to 250 characters.

    Common practice is to fill this from your SETUP_INFO.

    It is listed on https://www.lino-framework.org/apps.html

    """

    version = None
    url = None

    # mobile_server_url = None
    # """The URL to a mobile friedly version of the site.
    # Used instead of :attr:`server_url` when sending emails sent by
    # :class:`lino.modlib.notify.Message`
    # """

    device_type = 'desktop'
    """
    The default device type used on this server.  Should be one of
    ``'desktop'``, ``'tablet'`` or ``'mobile'``.

    This is used by :class:`DeviceTypeMiddleware
    <lino.core.auth.middleware.DeviceTypeMiddleware>`.
    """

    obj2text_template = "*{0}*"
    """The format template to use when rendering a ForeignKey as plain
    text.

    Note: reSTructuredText uses *italic* and **bold**.  Changing this
    can cause lots of trivial failures in test suites.  It is also
    used by :mod:`lino.modlib.notify` when generating the mail body.

    """

    migratable_plugin_prefixes = []
    """
    List of prefixes used in :manage:`initdb` and :cmd:`pm prep` command
    for plugins other then the plugins whose name startswith `lino`.
    For example: for plugins in welfare app, put 'welfare' in the list,
    so it the commands will prepare the postgres database properly.
    """

    make_missing_dirs = True
    """Set this to `False` if you don't want Lino to automatically create
    missing directories when needed.  If this is False, Lino will
    raise an exception in these cases, asking you to create it
    yourself.

    """
    userdocs_prefix = ''

    site_dir = None
    """The directory where Lino stores local files.
    See :ref:`dg.topics.local_files`.
    """

    project_dir = None
    """The :term:`Django project directory` for this site.
    See :ref:`dg.topics.local_files`.

    """

    media_root = None
    """The root directory at which to build the Javascript and json cache files.
    See :ref:`dg.topics.local_files`.
    """

    project_name = None
    """A nickname for this project.

    This is used only when :envvar:`LINO_CACHE_ROOT` is set, and only to set the
    :attr:`site_dir`.  In that case all Lino projects in a given repository must
    have a unique project name.

    If this is `None`, Lino will find a default value by splitting
    :attr:`project_dir` and taking the last part (or the second-last if the last
    part is 'settings'.

    """

    languages = None
    hidden_languages = None
    BABEL_LANGS = tuple()

    not_found_msg = '(not installed)'

    django_settings = None
    """This is a reference to the `globals()` dictionary of your
    :xfile:`settings.py` file (the one you provided when instantiating
    the Site object).

    """

    startup_time = None
    """
    The time when this Site has been instantiated,
    in other words the startup time of this Django process.
    Don't modify this.

    """

    plugins = None
    models = None

    top_level_menus = [
        ("master", _("Master")),
        ("main", None),
        ("reports", _("Reports")),
        ("config", _("Configure")),
        ("explorer", _("Explorer")),
        ("site", _("Site")),
    ]
    """The list of top-level menu items.
    See :doc:`/dev/menu` and :doc:`/dev/xlmenu`.
    """

    # is_local_project_dir = False
    # """Contains `True` if this is a "local" project.  For local projects,
    # Lino checks for local fixtures and config directories and adds
    # them to the default settings.

    # This is automatically set when a :class:`Site` is instantiated.

    # """

    ignore_model_errors = False
    """Not yet sure whether this is needed. Maybe when generating
    documentation.

    """

    loading_from_dump = False
    """Whether the process is currently loading data from a Python dump.

    When loading from a python dump, application code should not
    generate certain automatic data because that data is also part of
    the dump.

    This is normally `False`, but a Python dump created with
    :cmd:`pm dump2py` explicitly calls :meth:`install_migrations`,
    which sets this to `True`.

    Application code should not change this setting except for certain
    special test cases.

    """

    # see docs/settings.rst
    migration_class = None
    """
    If you maintain a data migrator module for your application,
    specify its name here.

    See :ref:`datamig` and/or :func:`lino.utils.dpy.install_migrations`.

    TODO: rename this to `migrator_class`

    """

    migrations_package = None
    """The full Python name of
    the local package that holds Django migrations for all plugins
    of this site.

    You might manually specify a name, but the recommended way is to create a
    :xfile:`migrations` directory.  See :doc:`/specs/migrate`.

    """

    partners_app_label = 'contacts'
    """
    Temporary setting, see :ref:`polymorphism`.
    """

    # three constants used by lino_xl.lib.workflows:
    max_state_value_length = 20
    max_action_name_length = 50
    max_actor_name_length = 100

    trusted_templates = False
    """
    Set this to True if you are sure that the users of your site won't try to
    misuse Jinja's capabilities.

    """

    uid = 'myuid'
    """A universal identifier for this Site.  This is needed when
    synchronizing with CalDAV server.  Locally created calendar
    components in remote calendars will get a UID based on this
    parameter, using ``"%s@%s" % (self.pk, settings.SITE.kernel)``.

    The default value is ``'myuid'``, and you should certainly
    override this on a production server that uses remote calendars.

    """

    project_model = None
    """
    Specifies the application's project model.

    A project in this context means what the users consider "the central most
    important thing that is used to classify most other things".  For example in
    :ref:`avanti` the "project" is a Client while in :ref:`tera` it is a
    therapy.

    This can be either `None` (the default value) or the full name of the model
    used as "central project model" in this application.

    If this is not `None`, all models that inherit from :class:`ProjectRelated
    <lino.mixins.ProjectRelated>` will have an additional ForeignKey to this
    model.

    TODO: convert this into a plugin setting of the office plugin?

    """

    user_model = None
    """
    The database model used for users.
    This is automatically set to ``'users.User'`` when
    :mod:`lino.modlib.users` is installed.

    Default value is `None`, meaning that this application has no user
    management.  See also :meth:`set_user_model`

    See also :doc:`/specs/users`.
    """

    # use_linod = False
    # """
    #
    # Whether this site uses the :mod:`lino.modlib.linod` plugin for ASGI
    # interface as well as an asynchronous lino daemon for background tasks and
    # logging. See: :mod:`lino.modlib.linod`.
    #
    # """

    # use_multiprocessing = False
    # """Whether to spawn a subprocess for certain secondary tasks.
    #
    # Don't use this. It is experimental and can cause disturbing side effects
    # like "The request's session was deleted before the request completed". See
    # :blogref:`20210616` for details.
    #
    # Currently used only by :meth:`lino.modlib.notify.Message.emit_notification`.
    #
    # """

    auth_middleware = None
    """
    Override used authorisation middlewares with supplied tuple of
    middleware class names.

    If None, use logic described in :ref:`admin.auth`

    """

    legacy_data_path = None
    """
    Used by custom fixtures that import data from some legacy
    database.

    """

    propvalue_max_length = 200
    """
    Used by :mod:`lino_xl.lib.properties`.
    """

    show_internal_field_names = True
    """Whether the internal field names should be visible.  ExtUI
    implements this by prepending them to the tooltip, which means
    that :attr:`use_quicktips` must also be `True`.  Default is
    `True`.

    """

    use_elasticsearch = False

    use_solr = False
    """

    Whether to use solr backend server for search document indexing.

    """

    developer_site_cache = None
    # build_js_cache_on_startup = None  # False
    # """Whether the :term:`site cache` should be populated on startup for
    # all user profiles and languages.
    #
    # """

    never_build_site_cache = False
    """
    Probably deprecated. Set this to `True` if you want that Lino never
    (re)builds the :term:`site cache`, even when asked.  This can be useful on a
    development server when you are debugging directly on the generated
    :xfile:`lino*.js`.  Or for certain unit test cases.

    """

    keep_erroneous_cache_files = False
    """Whether to keep partly generated files in the the :term:`site cache`.
    """

    use_java = True
    """
    A site-wide option to disable everything that needs Java.  Note
    that it is up to the plugins which include Java applications to
    respect this setting. Usage example is :mod:`lino_xl.lib.beid`.
    """

    use_silk_icons = False
    """
    If this is `True`, certain Lino plugins use the deprecated `silk
    icons library <http://www.famfamfam.com/lab/icons/silk/>`__ for
    representing workflows.

    The recommended but not yet fully implemented "modern" style is to
    use unicode symbols instead of icons.
    """

    use_new_unicode_symbols = False
    """Whether to use "new" unicode symbols (e.g. from the `Miscellaneous
    Symbols and Pictographs
    <https://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs>`__
    block) which are not yet implemented in all fonts.

    Currently used by :mod:`lino_noi.lib.noi.workflows`

    """

    use_experimental_features = False
    """Whether to include "experimental features". Deprecated.
    lino_xl.lib.inspect
    """
    site_config_defaults = {}
    """
    Default values to be used when creating the :attr:`site_config`.

    Usage example::

      site_config_defaults = dict(default_build_method='appypdf')


    """

    # default_build_method = "appypdf"
    # default_build_method = "appyodt"
    # default_build_method = "wkhtmltopdf"
    default_build_method = None
    """The default build method to use when rendering printable documents.

    This is the last default value, used only when
    :attr:`default_build_method
    <lino.modlib.system.SiteConfig.default_build_method>` in
    :class:`SiteConfig <lino.modlib.system.SiteConfig>` is
    empty.

    """

    is_demo_site = False
    """When this is `True`, then this site runs in "demo" mode.  "Demo
    mode" means:

    - the welcome text for anonymous users says "This demo site has X
      users, they all have "1234" as password", followed by a list of
      available usernames.

    Default value is `True`.  On a production site you will of course
    set this to `False`.

    See also :attr:`demo_fixtures` and :attr:`the_demo_date`.

    See also :attr:`quick_startup`.

    """

    demo_email = 'demo@example.com'

    # demo_fixtures = ['std', 'demo', 'demo2']
    demo_fixtures = []
    """
    The list of fixtures to be loaded by the :cmd:`pm prep`
    command.  See also :ref:`demo_fixtures`.

    """

    use_spinner = False  # doesn't work. leave this to False

    #~ django_admin_prefix = '/django'
    django_admin_prefix = None
    """
    The prefix to use for Django admin URLs.
    Leave this unchanged as long as :srcref:`docs/tickets/70` is not solved.
    """

    calendar_start_hour = 7
    """
    The first hour of a work day.

    Limits the choices of a :class:`lino.core.fields.CalendarTimeField`.
    """

    calendar_end_hour = 21
    """
    The last hour of a work day.

    Limits the choices of a :class:`lino.core.fields.CalendarTimeField`.

    """

    time_format_extjs = 'H:i'
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.

    """
    alt_time_formats_extjs = "g:ia|g:iA|g:i a|g:i A|h:i|g:i|H:i|ga|ha|gA|h a|g a|g A|gi|hi" \
                             "|gia|hia|g|H|gi a|hi a|giA|hiA|gi A|hi A" \
                             "|Hi|g.ia|g.iA|g.i a|g.i A|h.i|g.i|H.i"
    """Alternative time entry formats accepted by ExtJS time widgets.

    ExtJS default is:

        "g:ia|g:iA|g:i a|g:i A|h:i|g:i|H:i|ga|ha|gA|h a|g a|g A|gi|hi|gia|hia|g|H|gi a|hi a|giA|hiA|gi A|hi A"

    Lino's extended default also includes:

        "Hi" (1900) and "g.ia|g.iA|g.i a|g.i A|h.i|g.i|H.i" (Using . in replacement of ":")

    """
    date_format_extjs = 'd.m.Y'
    """Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.

    """

    alt_date_formats_extjs = 'd/m/Y|Y-m-d'
    """Alternative date entry formats accepted by ExtJS Date widgets.

    """

    default_number_format_extjs = '0,000.00/i'
    # default_number_format_extjs = '0,00/i'

    uppercase_last_name = False
    """
    Whether last name of persons should (by default) be printed with
    uppercase letters.  See :mod:`lino.test_apps.human`

    """

    jasmine_root = None
    """Path to the Jasmine root directory.  Only used on a development
    server if the `media` directory has no symbolic link to the
    Jasmine root directory and only if :attr:`use_jasmine` is True.

    """

    default_user = None
    """Username of the user to be used for all incoming requests.  Setting
    this to a nonempty value will disable authentication on this site.
    The special value `'anonymous'` will cause anonymous requests
    (whose `user` attribute is the :class:`AnonymousUser
    <lino.core.auth.utils.AnonymousUser>` singleton).

    See also :meth:`get_auth_method`.

    This setting should be `None` when :attr:`user_model` is `None`.

    """

    remote_user_header = None
    """The name of the header (set by the web server) that Lino should
    consult for finding the user of a request.  The default value
    `None` means that http authentication is not used.  Apache's
    default value is ``"REMOTE_USER"``.

    """

    # ldap_auth_server = None
    # """
    # This should be a string with the domain name and DNS (separated by a
    # space) of the LDAP server to be used for authentication.
    #
    # Example::
    #
    #   ldap_auth_server = 'DOMAIN_NAME SERVER_DNS'
    #
    # """

    use_gridfilters = True

    use_eid_applet = False
    """
    Whether to include functionality to read Belgian id cards using the
    official `eid-applet <http://code.google.com/p/eid-applet>`_.
    This option is experimental and doesn't yet work.  See
    `/blog/2012/1105`.
    """

    use_esteid = False
    """
    Whether to include functionality to read Estonian id cards.  This
    option is experimental and doesn't yet work.
    """

    # use_filterRow = not use_gridfilters
    # """
    # See `/blog/2011/0630`.
    # This option was experimental and doesn't yet work (and maybe never will).
    # """

    use_awesome_uploader = False
    """
    Whether to use AwesomeUploader.
    This option was experimental and doesn't yet work (and maybe never will).
    """

    use_tinymce = True
    """Replaced by :mod:`lino.modlib.tinymce`.
    """

    use_jasmine = False
    """Whether to use the `Jasmine <https://github.com/pivotal/jasmine>`_
    testing library.

    """

    use_quicktips = True
    """Whether to make use of `Ext.QuickTips
    <http://docs.sencha.com/ext-js/3-4/#!/api/Ext.QuickTips>`_ for
    displaying :ref:`help_texts` and internal field names (if
    :attr:`show_internal_field_names`).

    """

    use_css_tooltips = False
    """
    Whether to make use of CSS tooltips
    when displaying help texts defined in :class:`lino.models.HelpText`.
    """

    use_vinylfox = False
    """
    Whether to use VinylFox extensions for HtmlEditor.
    This feature was experimental and doesn't yet work (and maybe never will).
    See `/blog/2011/0523`.
    """

    # the following attributes are documented in hg/docs/admin/settings.py
    # default_ui = 'lino_extjs6.extjs6'
    default_ui = 'lino.modlib.extjs'
    # default_ui = 'lino.modlib.extjs'
    web_front_ends = None

    webdav_root = None
    webdav_url = None
    webdav_protocol = None
    use_security_features = False
    use_ipdict = False
    user_types_module = None
    workflows_module = None
    custom_layouts_module = None
    root_urlconf = 'lino.core.urls'
    social_auth_backends = None

    sidebar_width = 0
    """
    Used by :mod:`lino.modlib.plain`.
    Width of the sidebar in 1/12 of total screen width.
    Meaningful values are 0 (no sidebar), 2 or 3.

    """

    preview_limit = 15
    """
    Default value for the :attr:`preview_limit
    <lino.core.tables.AbstractTable.preview_limit>` parameter of all
    tables who don't specify their own one.  Default value is 15.
    """

    # admin_ui = None

    detail_main_name = 'main'

    bleach_allowed_tags = [
        'a', 'b', 'i', 'em', 'ul', 'ol', 'li', 'strong', 'p', 'br', 'span',
        'pre', 'def', 'div', 'img', 'table', 'th', 'tr', 'td', 'thead',
        'tfoot', 'tbody'
    ]
    """A list of tag names that are to *remain* in HTML comments if
    bleaching is active.

    See :doc:`/dev/bleach`.
    """

    ALLOWED_ATTRIBUTES['span'] = [
        'class', 'data-index', 'data-denotation-char', 'data-link',
        'data-title', 'data-value', 'contenteditable'
    ]
    ALLOWED_ATTRIBUTES['p'] = ["href", "title", "align"]

    bleach_allowed_attributes = ALLOWED_ATTRIBUTES
    """

    A dictionary of key-values for tagname-attributes_list which are to *remain*
    in HTML comments if bleaching is active.

    """

    textfield_bleached = True
    """Default value for `RichTextField.textfield_bleached`.

    See :doc:`/dev/bleach`.
    """
    textfield_format = 'plain'
    """
    The default format for text fields.  Valid choices are currently
    'plain' and 'html'.

    Text fields are either Django's `models.TextField` or
    :class:`lino.core.fields.RichTextField`.

    You'll probably better leave the global option as 'plain',
    and specify explicitly the fields you want as html by declaring
    them::

      foo = fields.RichTextField(..., format='html')

    We even recommend that you declare your *plain* text fields also
    using `fields.RichTextField` and not `models.TextField`::

      foo = fields.RichTextField()

    Because that gives subclasses of your application the possibility to
    make that specific field html-formatted::

       resolve_field('Bar.foo').set_format('html')
    """

    log_each_action_request = False
    """
    Whether Lino should log every incoming request for non
    :attr:`readonly <lino.core.actions.Action.readonly>` actions.

    This is experimental. Theoretically it is useless to ask Lino for logging
    every request since the web server does this. OTOH Lino can produce more
    readable logs.

    Note also that there is no warranty that actually *each* request is being
    logged.  It currently works only for requests that are being processed by
    the kernel's :meth:`run_action <lino.core.kernel.Kernel.run_action>`
    methods. """

    verbose_client_info_message = False
    """
    Set this to True if actions should send debug messages to the client.
    These will be shown in the client's Javascript console only.

    """

    stopsignal = "SIGTERM"
    """
    The signal to which the log server should register its shutdown handler.

    This is used when `_history_aware_logging` is enabled to log an info message
    when a process ends. And by the linod plugin to remove the socket file of
    the log server.

    On a production server with :setting:`linod.use_channels` is `True`, this
    must be the same signal as the ``stopsignal`` setting in the ``program``
    section of your `supervisor config
    <https://supervisord.org/configuration.html?highlight=stopsignal#program-x-section-values>`__.
    """

    help_url = "http://www.lino-framework.org"

    help_email = "users@lino-framework.org"
    """
    An e-mail address where users can get help. This is included in
    :xfile:`admin_main.html`.

    """

    catch_layout_exceptions = True
    """
    Lino usually catches any exception during startup (in
    :func:`create_layout_element
    <lino.core.layouts.create_layout_element>`) to report errors of
    style "Unknown element "postings.PostingsByController
    ('postings')" referred in layout <PageDetail on pages.Pages>."

    Setting this to `False` is useful when there's some problem
    *within* the framework.
    """

    strict_master_check = False
    """

    Whether to raise BadRequest when master instance is not correctly specified.
    This was introducted in March 2023 and is not yet implemented everywhere.

    """

    strict_dependencies = True
    """
    This should be True unless this site is being used just for autodoc
    or similar applications.
    """

    strict_choicelist_values = True
    """
    Whether invalid values in a ChoiceList should raise an exception.

    This should be `True` except for exceptional situations.  Setting this to
    `True` won't allow you to store invalid choicelist values in the database,
    but at least Lino will not raise an exception as soon as it reads an invalid
    value from existing data.  This can happen e.g. after a code upgrade without
    data migration.  In such a situation you may want to run
    :xfile:`make_snapshot.sh` in order to migrate the data.

    """

    csv_params = dict()
    """
    Site-wide default parameters for CSV generation.  This must be a
    dictionary that will be used as keyword parameters to Python
    `csv.writer()
    <http://docs.python.org/library/csv.html#csv.writer>`_

    Possible keys include:

    - encoding :
      the charset to use when responding to a CSV request.
      See
      http://docs.python.org/library/codecs.html#standard-encodings
      for a list of available values.

    - many more allowed keys are explained in
      `Dialects and Formatting Parameters
      <http://docs.python.org/library/csv.html#csv-fmt-params>`_.
    """

    logger_filename = 'lino.log'
    """
    The name of Lino's main log file, created in :meth:`setup_logging`.

    See also :ref:`host.logging`.
    """

    logger_format = '%(asctime)s %(levelname)s [%(name)s %(process)d %(thread)d] : %(message)s'
    """
    The format template to use for logging to the :xfile:`lino.log` file.
    """

    auto_configure_logger_names = 'atelier lino'
    """
    A string with a space-separated list of logger names to be
    automatically configured. See :meth:`setup_logging`.
    """

    log_sock_path = None
    """
    The full Path of the logger socket file (if this process is logging to the
    :term:`log server`), otherwise `None`.
    """

    # appy_params = dict(ooPort=8100)
    appy_params = dict(ooPort=8100,
                       pythonWithUnoPath='/usr/bin/python3',
                       raiseOnError=True)
    #~ decimal_separator = '.'
    decimal_separator = ','
    """
    Set this to either ``'.'`` or ``','`` to define wether to use comma
    or dot as decimal point separator when entering a `DecimalField`.
    """

    # decimal_group_separator = ','
    # decimal_group_separator = ' '
    # decimal_group_separator = '.'
    decimal_group_separator = "\u00A0"
    """
    Decimal group separator for :meth:`decfmt`.
    """

    time_format_strftime = '%H:%M'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.

    """

    date_format_strftime = '%d.%m.%Y'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.

    """

    date_format_regex = "/^[0123]?\d\.[01]?\d\.-?\d+$/"
    """
    Format (in Javascript regex syntax) to use for displaying dates to
    the user.  If you change this setting, you also need to override
    :meth:`parse_date`.

    """

    datetime_format_strftime = '%Y-%m-%dT%H:%M:%S'
    """
    Format (in strftime syntax) to use for formatting timestamps in
    AJAX responses.  If you change this setting, you also need to
    override :meth:`parse_datetime`.

    """

    datetime_format_extjs = 'Y-m-d\TH:i:s'
    """
    Format (in ExtJS syntax) to use for formatting timestamps in AJAX
    calls.  If you change this setting, you also need to override
    :meth:`parse_datetime`.

    """

    quick_startup = False
    """
    Whether to skip startup operations that are useful during development but
    not one production site.
    """

    master_site = None
    """Another Site instance to be used as the master for this site.
    :setting:`DATABASES` and :setting:`SECRET_KEY` and the :attr:`site_dir`
    """

    # for internal use:
    _logger = None
    _starting_up = False
    _hidden_plugins = None
    _shutdown_tasks = []
    """
    A set containing the names of plugins that are installed but inactive.
    """

    override_modlib_models = None
    """
    A dictionary which maps model class names to the plugin which
    overrides them.

    This is automatically filled at startup.  You can inspect it, but
    you should not modify it.  Needed for :meth:`is_abstract_model`.

    The challenge is that we want to know exactly where every model's
    concrete class will be defined *before* actually starting to
    import the :xfile:`models.py` modules.  That's why we need
    :attr:`extends_models <lino.core.plugin.Plugin.extends_models>`.

    This can be tricky, see e.g. 20160205.
    """

    installed_plugin_modules = None
    """
    Used internally by :meth:`is_abstract_model`.  Don't modify.

    A set of the full Python paths of all imported plugin modules. Not
    just the plugin modules themselves but also those they inherit
    from.
    """

    def __init__(self, settings_globals=None, local_apps=[], **kwargs):
        """Every Lino application calls this once in it's
        :file:`settings.py` file.
        See :doc:`/usage`.

        `settings_globals` is the `globals()` dictionary of your
        :xfile:`settings.py`.

        """

        # if hasattr(self, 'default_ui'):
        #     raise ChangedAPI("`default_ui` is replaced by `web_front_ends`")
        if hasattr(self, 'allow_duplicate_cities'):
            raise ChangedAPI(
                "allow_duplicate_cities is now a setting of the countries plugin"
            )
        if hasattr(self, 'setup_choicelists'):
            raise ChangedAPI("setup_choicelists is no longer supported")
        if hasattr(self, 'setup_workflows'):
            raise ChangedAPI("setup_workflows is no longer supported")
        if hasattr(self, 'beid_protocol'):
            raise ChangedAPI(
                "Replace Site.beid_protocol by plugins.beid.urlhandler_prefix")
        if hasattr(self, 'use_linod'):
            raise ChangedAPI(
                "Replace Site.use_linod by plugins.linod.use_channels")

        # if len(_INSTANCES):
        #     raise Exception("20161219")
        #     # happens e.g. during sphinx-build
        # _INSTANCES.append(self)
        # self.logger.info("20140226 Site.__init__() a %s", self)
        #~ print "20130404 ok?"
        if 'no_local' in kwargs:
            kwargs.pop('no_local')
            raise ChangedAPI("The no_local argument is no longer needed.")

        self._hidden_plugins = set()
        self._welcome_handlers = []
        self._quicklinks = None
        # self.features = AttrDict()
        self.plugins = AttrDict()
        self.models = AttrDict()
        self.modules = self.models  # backwards compat
        # self.actors = self.models  # backwards compat
        # self.actors = AttrDict()

        if isinstance(self.the_demo_date, (str, int)):
            self.the_demo_date = i2d(self.the_demo_date)

        if settings_globals is None:
            settings_globals = {}
        self.init_before_local(settings_globals, local_apps)
        self.setup_logging()
        self.run_lino_site_module()

        # for name, value in FEATURES_HOOKS.items():
        #     if hasattr(value, '__name__') and value.__name__ in ['activate_feature', 'deactivate_feature']:
        #         # Set default priority to a higher value so that site override other calls
        #         value.__defaults__ = value.__defaults__[:-1] + (10000,)
        #     if callable(value):
        #         setattr(self.__class__, name, classmethod(value))
        #     else:
        #         setattr(self.__class__, name, value)
        self.setup_features()
        self.override_settings(**kwargs)
        self.load_plugins()

        for p in self.installed_plugins:
            p.on_plugins_loaded(self)

        if self.migrations_package is None:
            MPNAME = "migrations"
            mpp = self.project_dir / MPNAME
            if mpp.exists():
                # parts = self.__module__.split('.')
                parts = os.getenv('DJANGO_SETTINGS_MODULE').split('.')
                # i = parts.index('settings')
                # mpn = '.'.join(parts[i]) + '.' + MPNAME
                mpn = '.'.join(parts[:-1]) + '.' + MPNAME
                # print("Local migrations package {} ({}).".format(mpn, mpp))
                self.migrations_package = mpn
                # self.migrations_package = self.__module__ + '.' + MPNAME
                # sm = import_module()
                # self.migrations_package = sm.__name__ + '.' + MPNAME
                fn = mpp / "__init__.py"
                if not fn.exists():
                    fn.write_text('')  # touch __init__ file.
            else:
                # print("No Django migrations because {} does not exist.".format(mpp))
                pass

        if self.migrations_package is not None:
            migrations_module = import_module(self.migrations_package)
            MIGRATION_MODULES = {}
            for p in self.installed_plugins:
                if p.app_label in ("contenttypes", "sessions", "staticfiles"):
                    # pure django plugins handle their own migrations
                    continue
                dir = join(migrations_module.__file__.rstrip("__init__.py"),
                           p.app_label)
                self.makedirs_if_missing(dir)
                open(join(dir, "__init__.py"),
                     "a").close()  # touch __init__ file.
                MIGRATION_MODULES[
                    p.app_label] = self.migrations_package + "." + p.app_label
            self.django_settings.update(MIGRATION_MODULES=MIGRATION_MODULES)

        self.setup_plugins()
        self.install_settings()

        for p in self.installed_plugins:
            if p.is_hidden():
                self._hidden_plugins.add(p.app_label)

        from lino.utils.config import ConfigDirCache
        self.confdirs = ConfigDirCache(self)

        for k in ('ignore_dates_before', 'ignore_dates_after'):
            if hasattr(self, k):
                msg = "{0} is no longer a site attribute"
                msg += " but a plugin attribute on lino_xl.lib.cal."
                msg = msg.format(k)
                raise ChangedAPI(msg)

        if self.title is None:
            self.title = self.project_name

    def init_before_local(self, settings_globals, local_apps):
        """If your :attr:`project_dir` contains no :xfile:`models.py`, but
        *does* contain a `fixtures` subdir, then Lino automatically adds this
        as a local fixtures directory to Django's :setting:`FIXTURE_DIRS`.

        But only once: if your application defines its own local
        fixtures directory, then this directory "overrides" those of
        parent applications. E.g. lino_noi.projects.care does not want
        to load the application-specific fixtures of
        lino_noi.projects.team.

        """
        if not isinstance(settings_globals, dict):
            raise Exception("""
            The first argument when instantiating a %s
            must be your settings.py file's `globals()`
            and not %r
            """ % (self.__class__.__name__, settings_globals))

        if isinstance(local_apps, str):
            local_apps = [local_apps]
        self.local_apps = local_apps

        self.django_settings = settings_globals
        project_file = settings_globals.get('__file__', '.')

        self.project_dir = Path(dirname(project_file)).absolute().resolve()

        # inherit `project_name` from parent?
        # if self.__dict__.get('project_name') is None:
        if self.project_name is None:
            parts = reversed(str(self.project_dir).split(os.sep))
            # print(20150129, list(parts))
            for part in parts:
                if part != 'settings':
                    self.project_name = part
                    break

        if self.master_site is None:
            cache_root = os.environ.get('LINO_CACHE_ROOT', None)
            if cache_root:
                # TODO: deprecate
                cr = Path(cache_root).absolute()
                if not cr.exists():
                    msg = "LINO_CACHE_ROOT ({0}) does not exist!".format(cr)
                    raise Exception(msg)
                self.site_dir = (cr / self.project_name).resolve()
                self.setup_cache_directory()
            else:
                self.site_dir = self.project_dir
            db = self.get_database_settings()
            if db is not None:
                self.django_settings.update(DATABASES=db)

        else:
            self.site_dir = self.master_site.site_dir
            self._history_aware_logging = self.master_site._history_aware_logging
            for k in ('DATABASES', 'SECRET_KEY'):
                self.django_settings[k] = self.master_site.django_settings[k]

        self.update_settings(SERIALIZATION_MODULES={
            "py": "lino.utils.dpy",
        })

        # before Django 3.2 an automatic id was always django.db.models.AutoField
        # self.update_settings(DEFAULT_AUTO_FIELD='django.db.models.AutoField')
        self.update_settings(
            DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')

        if self.site_prefix != '/':
            if not self.site_prefix.endswith('/'):
                raise Exception("`site_prefix` must end with a '/'!")
            if not self.site_prefix.startswith('/'):
                raise Exception("`site_prefix` must start with a '/'!")
            self.update_settings(SESSION_COOKIE_PATH=self.site_prefix[:-1])
            # self.update_settings(SESSION_COOKIE_NAME='ssid')

        self.VIRTUAL_FIELDS = set()
        self._startup_done = False
        self.startup_time = datetime.datetime.now()

    def setup_logging(self):
        """Modifies the :data:`DEFAULT_LOGGING
        <django.utils.log.DEFAULT_LOGGING>` setting.

        This is called *before* any plugins are loaded because all this must
        happen *before* Django passes the setting to the
        `logging.config.dictConfig
        <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`__
        function.

        It is designed to work with the :setting:`LOGGING` and
        :setting:`LOGGER_CONFIG` settings unmodified.

        It does the following modifications:

        - Define a *default logger configuration* that is initially the same as
          the one used by Django::

            {
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
            }

        - If the :attr:`site_dir` has a subdirectory named ``log``,
          and if :attr:`logger_filename` is not empty, add a handler
          named ``file`` and a formatter named ``verbose``, and add
          that handler to the default logger configuration.

        - Apply the default logger configuration to every logger name
          in :attr:`auto_configure_logger_names`.

        - (does no longer) configure the console handler to write to stdout
          instead of Django's default stderr (as explained `here
          <http://codeinthehole.com/writing/console-logging-to-stdout-in-django/>`__)
          because that breaks testing.

        It does nothing at all if :attr:`auto_configure_logger_names`
        is set to `None` or empty.

        See also :ref:`host.logging`.

        """
        if not self.auto_configure_logger_names:
            return

        if len(logging.root.handlers) > 0:

            # Logging has been configured by something else. This can happen
            # when Site is instantiated a second time. Or accidentaly (e.g. when you call logging.basicConfig() in the settings.py), Or when some testing
            # environment runs multiple doctests in a same process.  We don't
            # care, we restart configuration from scratch.

            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)

        from django.utils.log import DEFAULT_LOGGING
        d = DEFAULT_LOGGING

        if d.get('logger_ok', False):
            # raise Exception("20231017")
            return

        level = os.environ.get('LINO_LOGLEVEL', 'INFO').upper()
        file_level = os.environ.get('LINO_FILE_LOGLEVEL', level).upper()
        min_level = min(*[getattr(logging, k) for k in (level, file_level)])

        # print("20231017 level is", level)

        loggercfg = {
            'handlers': ['console', 'mail_admins'],
            'level': logging.getLevelName(min_level),
        }

        handlers = d.setdefault('handlers', {})
        if True:
            # We override Django's default config: write to stdout (not
            # stderr) and remove the 'require_debug_true' filter.
            console = handlers.setdefault('console', {})
            console['stream'] = sys.stdout
            if 'filters' in console:
                del console['filters']
            console['level'] = level

        # when Site is instantiated several times, we keep the existing file handler
        # print("20231016", self.logger_filename, handlers.keys())
        if self.logger_filename and 'file' not in handlers:
            logdir = self.site_dir / 'log'
            if logdir.is_dir():
                # print("20231019", self, "logdir is", logdir)
                self._history_aware_logging = True
                log_file_path = logdir / self.logger_filename
                self.log_sock_path = logdir / (self.logger_filename + '.sock')
                # if is_logserver() or not self.log_sock_path.exists():
                if self.log_sock_path.exists():
                    # print("20231019 logging to socket server", file_level)
                    handlers['file'] = {
                        'class': 'lino.core.site.LinoSocketHandler',
                        'host': str(self.log_sock_path),
                        'port': None,
                        'level': file_level
                    }
                else:
                    # print("20231019 logging to lino.log", file_level)
                    formatters = d.setdefault('formatters', {})
                    formatters.setdefault(
                        'verbose',
                        dict(format=self.logger_format,
                             datefmt='%Y%m-%d %H:%M:%S'))
                    handlers['file'] = {
                        'level': file_level,
                        'class': 'logging.handlers.WatchedFileHandler',
                        'filename': str(log_file_path),
                        'encoding': 'UTF-8',
                        'formatter': 'verbose',
                    }

        # when a file handler exists, we have the loggers use it even if this
        # instance didn't create it:
        if 'file' in handlers:
            loggercfg['handlers'].append('file')

        for name in self.auto_configure_logger_names.split():
            # if name not in d['loggers']:
            d['loggers'][name] = loggercfg

        dblogger = d['loggers'].setdefault('django.db.backends', {})
        dblogger['level'] = os.environ.get('LINO_SQL_LOGLEVEL', 'WARNING')
        dblogger['handlers'] = loggercfg['handlers']

        # # https://code.djangoproject.com/ticket/30554
        # logger = d['loggers'].setdefault('django.utils.autoreload', {})
        # logger['level'] = 'INFO'

        # if 'linod' in d['loggers']:
        #     for item in d['loggers'].keys():
        #         if item not in ['linod', 'root']:
        #             d['loggers'][item]['propagate'] = True

        if ASYNC_LOGGING:
            config = d.copy()

            try:
                logging.config.dictConfig(config)
                # logging.config.dictConfig(d)
            finally:
                d.clear()
                d['logger_ok'] = True
                d['version'] = 1
                d['disable_existing_loggers'] = False
        else:
            d['logger_ok'] = True
        # self.update_settings(LOGGING=d)
        # from pprint import pprint
        # pprint(d)
        # print("20161126 Site %s " % d['loggers'].keys())
        # import yaml
        # print("20231019", yaml.dump(d))

    def get_database_settings(self):
        """Return a dict to be set as the :setting:`DATABASE` setting.

        The default behaviour uses SQLite (1) on a file named
        :xfile:`default.db` in the :attr:`site_dir` if that attribute is
        specified, and (2) in ``:memory:`` when :attr:`site_dir` is `None`.

        And alternative might be for example::

            def get_database_settings(self):
                return {
                    'default': {
                        'ENGINE': 'django.db.backends.mysql',
                        'NAME': 'test_' + self.project_name,
                        'USER': 'django',
                        'PASSWORD': os.environ['MYSQL_PASSWORD'],
                        'HOST': 'localhost',
                        'PORT': 3306,
                        'OPTIONS': {
                           "init_command": "SET storage_engine=MyISAM",
                        }
                    }
                }

        """
        if self.site_dir is None:
            pass  # raise Exception("20160516 No site_dir")
        else:
            dbname = self.site_dir / 'default.db'
            return {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': str(dbname)
                }
            }

    def get_anonymous_user(self):
        # The code below works even when users is not installed
        from lino.modlib.users.choicelists import UserTypes
        return UserTypes.get_anonymous_user()

    def run_lino_site_module(self):
        """Deprecated. Probably no longer used. See :ref:`lino.site_module`.

        """
        site_module = os.environ.get('LINO_SITE_MODULE', None)
        if site_module:
            mod = import_module(site_module)
            func = getattr(mod, 'setup_site', None)
            if func:
                func(self)
        # try:
        #     from djangosite_local import setup_site
        # except ImportError:
        #     pass
        # else:
        #     setup_site(self)

    def override_settings(self, **kwargs):
        # Called internally during `__init__` method.
        # Also called from :mod:`lino.utils.djangotest`

        #~ logger.info("20130404 lino.site.Site.override_defaults")

        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self.__class__, k))
            setattr(self, k, v)

        self.apply_languages()

    def get_plugin_configs(self):
        return []

    def load_plugins(self):
        """Load all plugins and build the :setting:`INSTALLED_APPS` setting
        for Django.

        This includes a call to :meth:`get_apps_modifiers` and
        :meth:`get_installed_apps`.

        """
        # Called internally during `__init__` method.

        if hasattr(self, 'hidden_apps'):
            raise ChangedAPI("Replace hidden_apps by get_apps_modifiers()")

        def setpc(pc):
            if isinstance(pc, tuple):
                if len(pc) != 3:
                    raise Exception("20190318")
                app_label, k, value = pc
                d = PLUGIN_CONFIGS.setdefault(app_label, {})
                d[k] = value
            else:  # expect an iterable returned by super()
                for x in pc:
                    setpc(x)

        for pc in self.get_plugin_configs():
            setpc(pc)

        cfgp = ConfigParser()
        cfgp.read(self.project_dir / 'lino.ini')
        for section in cfgp.sections():
            if section.startswith('getlino') or section == 'DEFAULT':
                continue
            if section not in PLUGIN_CONFIGS:
                PLUGIN_CONFIGS[section] = dict()
            for option in cfgp.options(section):
                PLUGIN_CONFIGS[section][option] = cfgp.parsed_get(
                    section, option)

        requested_apps = []
        apps_modifiers = self.get_apps_modifiers()

        def add(x):
            if isinstance(x, str):
                app_label = x.split('.')[-1]
                x = apps_modifiers.pop(app_label, x)
                if x is not None:
                    requested_apps.append(x)
            else:
                # if it's not a string, then it's an iterable of strings
                for xi in x:
                    add(xi)

        for x in self.get_installed_apps():
            add(x)

        for x in self.local_apps:
            add(x)

        # actual_apps = []
        plugins = []

        # disabled_plugins = set()

        def install_plugin(app_name, needed_by=None):
            # print("20210305 install_plugin({})".format(app_name))
            # Django does not accept newstr, and we don't want to see
            # ``u'applabel'`` in doctests.
            app_name = str(app_name)
            # print("20160524 install_plugin(%r)" % app_name)
            app_mod = import_module(app_name)

            # print "Loading plugin", app_name
            k = app_name.rsplit('.')[-1]
            x = apps_modifiers.pop(k, 42)
            if x is None:
                return
            elif x == 42:
                pass
            else:
                raise Exception("20160712")
            if k in self.plugins:
                other = self.plugins[k]
                if other.app_name == app_name:
                    # If a plugin is installed more than once, only
                    # the first one counts and all others are ignored
                    # silently. Happens e.g. in Lino Noi where
                    # lino_noi.lib.noi is both a required plugin and
                    # the default_ui.
                    return
                raise Exception("Tried to install {} where {} "
                                "is already installed.".format(
                                    app_name, other))

            # Can an `__init__.py` file explicitly set ``Plugin =
            # None``? Is that feature being used?
            app_class = getattr(app_mod, 'Plugin', None)
            if app_class is None:
                app_class = Plugin
            cfg = PLUGIN_CONFIGS.pop(k, None)
            ip = app_class(self, k, app_name, app_mod, needed_by, cfg
                           or dict())
            # cfg = PLUGIN_CONFIGS.pop(k, None)
            # if cfg:
            #     ip.configure(**cfg)

            self.plugins.define(k, ip)

            needed_by = ip
            # while needed_by.needed_by is not None:
            #     needed_by = needed_by.needed_by
            for dep in ip.get_required_plugins():
                k2 = dep.rsplit('.')[-1]
                if k2 not in self.plugins:
                    install_plugin(dep, needed_by=needed_by)
                    # plugins.append(dep)

            plugins.append(ip)
            # for dp in ip.disables_plugins:
            #     disabled_plugins.add(dp)

        # lino is always the first plugin:
        install_plugin('lino')

        for app_name in requested_apps:
            install_plugin(app_name)

        # raise Exception("20190318 {} {}".format([p.app_label for p in plugins], ''))

        if apps_modifiers:
            raise Exception(
                "Invalid app_label '{0}' in your get_apps_modifiers!".format(
                    list(apps_modifiers.keys())[0]))

        # The return value of get_auth_method() may depend on a
        # plugin, so if needed we must add the django.contrib.sessions
        # afterwards.
        # if self.get_auth_method() == 'session':
        if self.user_model:
            k = str('django.contrib.sessions')
            if k not in self.plugins:
                install_plugin(k)

        # for p in plugins:
        #     if p.app_label in disabled_plugins \
        #        or p.app_name in disabled_plugins:
        #         plugins.remove(p)
        #         del self.plugins[p.app_label]

        # self.update_settings(INSTALLED_APPS=tuple(actual_apps))
        self.update_settings(
            INSTALLED_APPS=tuple([p.app_name for p in plugins]))
        self.installed_plugins = tuple(plugins)

        if self.override_modlib_models is not None:
            raise ChangedAPI("override_modlib_models no longer allowed")

        self.override_modlib_models = dict()

        # def reg(p, pp, m):
        #     name = pp.__module__ + '.' + m
        #     self.override_modlib_models[name] = p

        def plugin_parents(pc):
            for pp in pc.__mro__:
                if issubclass(pp, Plugin):
                    # if pp not in (Plugin, p.__class__):
                    if pp is not Plugin:
                        yield pp

        def reg(pc):
            # If plugin p extends some models, then tell all parent
            # plugins to make their definition of each model abstract.
            extends_models = pc.__dict__.get('extends_models')
            if extends_models is not None:
                for m in extends_models:
                    if "." in m:
                        raise Exception("extends_models in %s still uses '.'" %
                                        pc)
                    for pp in plugin_parents(pc):
                        if pp is pc:
                            continue
                        name = pp.__module__ + '.' + m
                        self.override_modlib_models[name] = pc
                        # if m == "Company":
                        #     print("20160524 tell %s that %s extends %s" % (
                        #         pp, p.app_name, m))

            for pp in plugin_parents(pc):
                if pp is pc:
                    continue
                reg(pp)

            # msg = "{0} declares to extend_models {1}, but " \
            #       "cannot find parent plugin".format(p, m)
            # raise Exception(msg)

        for p in self.installed_plugins:
            reg(p.__class__)
            # for pp in plugin_parents(p.__class__):
            #     if p.app_label == 'contacts':
            #         print("20160524c %s" % pp)
            #     reg(p.__class__)

        # for m, p in self.override_modlib_models.items():
        #     print("20160524 %s : %s" % (m, p))

        self.installed_plugin_modules = set()
        for p in self.installed_plugins:
            self.installed_plugin_modules.add(p.app_module.__name__)
            for pp in plugin_parents(p.__class__):
                self.installed_plugin_modules.add(pp.__module__)

        # print("20160524 %s", self.installed_plugin_modules)
        # raise Exception("20140825 %s", self.override_modlib_models)

    def get_requirements(self):
        """
        Collect requirements from plugins. Add some more requirements which
        depend on options in the local :xfile:`settings.py` file.
        """
        reqs = set()
        for p in self.installed_plugins:
            for r in p.get_requirements(self):
                reqs.add(r)
        if self.textfield_bleached:
            reqs.add("bleach")
        return sorted(reqs)

    def unused_load_actors(self):
        """Collect :xfile:`desktop.py` modules.

        Deprecated. We plan to remove the design_name attribute.

        Note the situation when a :xfile:`desktop.py` module exists
        but causes itself an ImportError because it contains a
        programming mistake. In that case we want the traceback to
        occur, not to silently do as if no :xfile:`desktop.py` module
        existed.

        """
        for p in self.installed_plugins:
            mn = p.app_name + '.' + self.design_name
            fn = join(dirname(p.app_module.__file__), self.design_name + '.py')
            if exists(fn):
                # self.actors[p.app_label] = import_module(mn)
                m = import_module(mn)
                d = m.__dict__.copy()
                for key in m.__dict__:
                    if key.startswith('__'):
                        d.pop(key)
                self.models[p.app_label].__dict__.update(d)
            # try:
            #     # print("20160725 Loading actors from", mn)
            #     self.actors[p.app_label] = import_module(mn)
            # except ImportError:
            #     pass

    def setup_plugins(self):
        """
        Deprecated. Use :meth:`get_plugin_configs` instead.

        This method is called exactly once during site startup, after
        :meth:`load_plugins` but before populating the models
        registry.

        See :ref:`dev.plugins`.


        """
        pass

    def install_settings(self):

        assert not self.help_url.endswith('/')

        for p in self.installed_plugins:
            p.install_django_settings(self)

        # import django
        # django.setup()
        if self.site_dir is not None:
            self.media_root = self.site_dir / 'media'
            if self.webdav_url is None:
                self.webdav_url = self.site_prefix + 'media/webdav/'
            if self.webdav_root is None:
                self.webdav_root = self.media_root / 'webdav'
            self.update_settings(MEDIA_ROOT=str(self.media_root))

        self.update_settings(ROOT_URLCONF=self.root_urlconf)
        self.update_settings(MEDIA_URL='/media/')

        if not 'STATIC_ROOT' in self.django_settings:
            cache_root = os.environ.get('LINO_CACHE_ROOT', None)
            if cache_root:
                p = Path(cache_root)
            else:
                p = self.site_dir
            self.update_settings(STATIC_ROOT=str(p / 'static_root'))
        if not 'STATIC_URL' in self.django_settings:
            self.update_settings(STATIC_URL='/static/')

        if not 'USE_TZ' in self.django_settings:
            # django.utils.deprecation.RemovedInDjango50Warning: The default
            # value of USE_TZ will change from False to True in Django 5.0. Set
            # USE_TZ to False in your project settings if you want to keep the
            # current default behavior.
            self.update_settings(USE_TZ=False)

        # loaders = [
        #     'lino.modlib.jinja.loader.Loader',
        #     'django.template.loaders.filesystem.Loader',
        #     'django.template.loaders.app_directories.Loader',
        #     #~ 'django.template.loaders.eggs.Loader',
        # ]

        tcp = []

        tcp += [
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        ]
        # self.update_settings(TEMPLATE_LOADERS=tuple(loaders))
        # self.update_settings(TEMPLATE_CONTEXT_PROCESSORS=tuple(tcp))

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': tcp,
                    # 'loaders': loaders
                },
            },
        ]
        TEMPLATES.append({
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'DIRS': [],
            'OPTIONS': {
                'environment': 'lino.modlib.jinja.get_environment'
            },
        })

        self.update_settings(TEMPLATES=TEMPLATES)

        if self.user_model:
            self.update_settings(AUTH_USER_MODEL='users.User')
            if self.use_security_features:
                self.update_settings(CSRF_USE_SESSIONS=True,
                                     SESSION_COOKIE_SECURE=True,
                                     CSRF_COOKIE_SECURE=True)

        # self.define_settings(AUTH_USER_MODEL=self.user_model)

        self.define_settings(MIDDLEWARE=tuple(self.get_middleware_classes()))

        # if self.get_auth_method() == 'session':
        #     self.define_settings(AUTHENTICATION_BACKENDS=[
        #         'django.contrib.auth.backends.RemoteUserBackend'
        #     ])

        backends = []
        # if self.use_ipdict:
        #     backends.append('lino.modlib.ipdict.backends.Backend')
        if self.get_auth_method() == 'remote':
            backends.append('lino.core.auth.backends.RemoteUserBackend')
        else:
            backends.append('lino.core.auth.backends.ModelBackend')

        if self.social_auth_backends is not None:
            backends += self.social_auth_backends

        self.define_settings(AUTHENTICATION_BACKENDS=backends)

        self.update_settings(
            LOGIN_URL='/accounts/login/',
            LOGIN_REDIRECT_URL=self.site_prefix,
            # LOGIN_REDIRECT_URL = '/accounts/profile/',
            LOGOUT_REDIRECT_URL=None)

        def collect_settings_subdirs(lst, name, max_count=None):

            def add(p):
                p = p.replace(os.sep, "/")
                if p not in lst:
                    lst.append(p)

            for p in self.get_settings_subdirs(name):
                # if the parent of a settings subdir has a
                # `models.py`, then it is a plugin and we must not add
                # the subdir because Django does that.
                if exists(join(p, '..', 'models.py')):
                    self.logger.debug(
                        "Not loading %s %s because Django does that", p, name)
                else:
                    add(str(p))
                    if (max_count is not None) and len(lst) >= max_count:
                        break

            # local_dir = self.site_dir.child(name)
            # if local_dir.exists():
            #     print "20150427 adding local directory %s" % local_dir
            #     add(local_dir)
            # The STATICFILES_DIRS setting should not contain the
            # STATIC_ROOT setting

            if False:
                # If a plugin has no "fixtures" ("config") directory
                # of its own, inherit it from parents.  That would be
                # nice and it even works, but with a stud: these
                # fixtures will be loaded at the end.
                for ip in self.installed_plugins:
                    if not ip.get_subdir(name):
                        pc = ip.extends_from()
                        while pc and issubclass(pc, Plugin):
                            p = pc.get_subdir(name)
                            if p:
                                add(p)
                            pc = pc.extends_from()

        fixture_dirs = list(self.django_settings.get('FIXTURE_DIRS', []))
        locale_paths = list(self.django_settings.get('LOCALE_PATHS', []))
        # sfd = list(self.django_settings.get('STATICFILES_DIRS', []))
        # sfd.append(self.site_dir.child('genjs'))
        collect_settings_subdirs(fixture_dirs, 'fixtures', 1)
        collect_settings_subdirs(locale_paths, 'locale')
        # collect_settings_subdirs(sfd, 'static')
        self.update_settings(FIXTURE_DIRS=tuple(fixture_dirs))
        self.update_settings(LOCALE_PATHS=tuple(locale_paths))
        # root = self.django_settings['STATIC_ROOT']
        # sfd = tuple([x for x in sfd if x != root])
        # self.update_settings(STATICFILES_DIRS=sfd)

        # if self.build_js_cache_on_startup or self.never_build_site_cache:
        #     sfd = list(self.django_settings.get('STATICFILES_DIRS', []))
        #     sfd.append(self.media_root)
        #     self.update_settings(STATICFILES_DIRS=sfd)

        # print(20150331, self.django_settings['FIXTURE_DIRS'])

    def setup_cache_directory(self):
        """When :envvar:`LINO_CACHE_ROOT` is set, Lino adds a stamp file
        called :xfile:`lino_cache.txt` to every project's cache
        directory in order to avoid duplicate use of same cache
        directory.

        .. xfile:: lino_cache.txt

            A small text file with one line of text which contains the
            path of the project which uses this cache directory.

        """

        stamp = self.site_dir / 'lino_cache.txt'
        this = class2str(self.__class__)
        if stamp.exists():
            other = stamp.read_file()
            if other == this:
                ok = True
            else:
                ok = False
                for parent in self.__class__.__mro__:
                    if other == class2str(parent):
                        ok = True
                        break
            if not ok:
                # Can happen e.g. when `python -m lino.hello` is
                # called.  in certain conditions.
                msg = ("Cannot use {site_dir} for {this} "
                       "because it is used for {other}. (Settings {settings})")
                msg = msg.format(
                    site_dir=self.site_dir,
                    this=this,
                    settings=self.django_settings.get('SETTINGS_MODULE'),
                    other=other)
                if True:
                    raise Exception(msg)
                else:
                    # print(msg)
                    self.site_dir = None
        else:
            self.makedirs_if_missing(self.site_dir)
            stamp.write_file(this)

    def set_user_model(self, spec):
        """This can be called during the :meth:`on_init
        <lino.core.plugin.Plugin.on_init>` of plugins that provide
        user management (the only plugin that does this is currently
        :mod:`lino.modlib.users`).

        """
        # if self.user_model is not None:
        #     msg = "Site.user_model was already set!"
        #     Theoretically this should raise an exception. But in a
        #     transitional phase after 20150116 we just ignore it. A
        #     warning would be nice, but we cannot use the logger here
        #     since it is not yet configured.
        #     self.logger.warning(msg)
        #     raise Exception(msg)
        self.user_model = spec
        if self.user_types_module is None:
            self.user_types_module = 'lino.core.user_types'

    def get_auth_method(self):
        """Returns the authentication method used on this site. This is one of
        `None`, `'remote'` or `'session'`.

        It depends on the values in
        :attr:`user_model`,
        :attr:`default_user` and
        :attr:`remote_user_header`.

        It influences the results of
        :meth:`get_middleware_classes` and
        :meth:`get_installed_apps`, and the content of
        :setting:`AUTHENTICATION_BACKENDS`.

        """
        if self.user_model is None:
            return None
        if self.default_user is not None:
            return None
        if self.remote_user_header is None:
            return 'session'  # model backend
        return 'remote'  # remote user backend

    def get_apps_modifiers(self, **kwargs):
        return kwargs

    def is_hidden_plugin(self, app_label):
        return app_label in self._hidden_plugins

    def is_hidden_app(self, app_label):
        """

        Return True if the named plugin is installed, known, but has been disabled using
        :meth:`get_apps_modifiers`.

        """
        am = self.get_apps_modifiers()
        if am.get(app_label, 1) is None:
            return True

    def update_settings(self, **kw):
        """This may be called from within a :xfile:`lino_local.py`.

        """
        self.django_settings.update(**kw)

    def define_settings(self, **kwargs):
        """Same as :meth:`update_settings`, but raises an exception if a
        setting already exists.

        TODO: Currently this exception is deactivated.  Because it
        doesn't work as expected.  For some reason (maybe because
        settings is being imported twice on a devserver) it raises a
        false exception when :meth:`override_defaults` tries to use it
        on :setting:`MIDDLEWARE_CLASSES`...

        """
        if False:
            for name in kwargs.keys():
                if name in self.django_settings:
                    raise Exception(
                        "Tried to define existing Django setting %s" % name)
        self.django_settings.update(kwargs)

    def startup(self):
        """Start up this Site.

        You probably don't want to override this method as it might be
        called several times.  e.g. under mod_wsgi: another thread has
        started and not yet finished `startup()`.

        If you want to run custom code on
        site startup, override :meth:`do_site_startup`.

        """
        from lino.core.kernel import site_startup
        site_startup(self)
        if self.site_locale:
            try:
                locale.setlocale(locale.LC_ALL, self.site_locale)
            except locale.Error as e:
                self.logger.warning("%s : %s", self.site_locale, e)
        self.clear_site_config()

    def register_shutdown_task(self, task):
        self._shutdown_tasks.append(task)

    def shutdown(self):
        for t in self._shutdown_tasks:
            t()

    def do_site_startup(self):
        """
        This method is called exactly once during site startup, just
        between the pre_startup and the post_startup signals.  A hook
        for subclasses.

        TODO: rename this to `on_startup`?

        """

        # self.logger.info("20160526 %s do_site_startup() a", self.__class__)
        # self.logger.info("20160526 %s do_site_startup() b", self.__class__)

    logger = logger  # backwards-compat. Don't use this.

    def get_settings_subdirs(self, subdir_name):
        """Yield all (existing) directories named `subdir_name` of this Site's
        project directory and its inherited project directories.

        """

        found = set()
        # print("20200701 compare", self.site_dir, classdir(self.__class__))
        # if self.site_dir != classdir(self.__class__):
        if True:
            pth = self.project_dir / subdir_name
            if pth.is_dir():
                yield pth
                # print("20200701 found", pth)
                found.add(pth)

        # If the settings.py doesn't subclass Site, then we also want to get
        # the inherited subdirs.
        for cl in self.__class__.__mro__:
            # print("20130109 inspecting class %s" % cl)
            if cl is not object and not inspect.isbuiltin(cl):
                pth = join(classdir(cl), subdir_name)
                if isdir(pth) and not pth in found:
                    # if isdir(pth):
                    yield pth
                    found.add(pth)

    def makedirs_if_missing(self, dirname):
        """Make missing directories if they don't exist and if
        :attr:`make_missing_dirs` is `True`.

        """
        if dirname and not isdir(dirname):
            if self.make_missing_dirs:
                os.makedirs(dirname)
            else:
                raise Exception("Please create yourself directory %s" %
                                dirname)

    def is_abstract_model(self, module_name, model_name):
        """
        Return True if the named model is declared as being extended by
        :attr:`lino.core.plugin.Plugin.extends_models`.

        Typical usage::

            class MyModel(dd.Model):
                 class Meta:
                     abstract = dd.is_abstract_model(__name__, 'MyModel')

        See :doc:`/dev/plugin_inheritance`.
        """
        app_name = '.'.join(module_name.split('.')[:-1])
        model_name = app_name + '.' + model_name
        # if 'avanti' in model_name:
        #     print("20170120", model_name,
        #           self.override_modlib_models,
        #           [m for m in self.installed_plugin_modules])
        rv = model_name in self.override_modlib_models
        if not rv:
            if app_name not in self.installed_plugin_modules:
                return True
        # if model_name.endswith('Company'):
        #     self.logger.info(
        #         "20160524 is_abstract_model(%s) -> %s", model_name, rv)
        # self.logger.info(
        #     "20160524 is_abstract_model(%s) -> %s (%s, %s)",
        #     model_name, rv, self.override_modlib_models.keys(),
        #     os.getenv('DJANGO_SETTINGS_MODULE'))
        return rv

    def is_installed_model_spec(self, model_spec):
        """
        Deprecated. This feature was a bit too automagic and caused bugs
        to pass silently.  See e.g. :blogref:`20131025`.
        """
        if False:  # mod_wsgi interprets them as error
            warnings.warn("is_installed_model_spec is deprecated.",
                          category=DeprecationWarning)

        if model_spec == 'self':
            return True
        app_label, model_name = model_spec.split(".")
        return self.is_installed(app_label)

    def is_installed(self, app_label):
        """
        Return `True` if :setting:`INSTALLED_APPS` contains an item
        which ends with the specified `app_label`.

        """
        if self.installed_plugin_modules is None:
            raise Exception("Plugins are not yet loaded.")
        return app_label in self.plugins

    def setup_model_spec(self, obj, name):
        """
        If the value of the named attribute of `obj` is a string, replace
        it by the model specified by that string.

        Example usage::

            # library code:
            class ThingBase(object):
                the_model = None

                def __init__(self):
                    settings.SITE.setup_model_spec(self, 'the_model')

            # user code:
            class MyThing(ThingBase):
                the_model = "contacts.Partner"
        """
        spec = getattr(obj, name)
        if spec and isinstance(spec, str):
            if not self.is_installed_model_spec(spec):
                setattr(obj, name, None)
                return
            from lino.core.utils import resolve_model
            msg = "Unresolved model '%s' in {0}.".format(name)
            msg += " ({})".format(str(self.installed_plugins))
            setattr(obj, name, resolve_model(spec, strict=msg))

    def on_each_app(self, methname, *args):
        """
        Call the named method on the :xfile:`models.py` module of each
        installed app.

        Note that this mechanism is deprecated. It is still used (on
        names like ``setup_workflows`` and ``setup_site``) for
        historical reasons but will disappear one day.
        """
        from django.apps import apps
        apps = [a.models_module for a in apps.get_app_configs()]
        for mod in apps:
            meth = getattr(mod, methname, None)
            if meth is not None:
                if False:  # 20150925 once we will do it for good...
                    raise ChangedAPI("{0} still has a function {1}".format(
                        mod, methname))
                meth(self, *args)

    def for_each_app(self, func, *args, **kw):
        """
        Call the given function on each installed plugin.  Successor of
        :meth:`on_each_app`.

        This also loops over plugins that don't have a models module
        and the base plugins of plugins which extend some plugin.
        """

        from importlib import import_module
        done = set()
        for p in self.installed_plugins:
            for b in p.__class__.__mro__:
                if b not in (object, Plugin):
                    if b.__module__ not in done:
                        done.add(b.__module__)
                        parent = import_module(b.__module__)
                        func(b.__module__, parent, *args, **kw)
            if p.app_name not in done:
                func(p.app_name, p.app_module, *args, **kw)

    def demo_date(self, *args, **kwargs):
        """
        Deprecated. Should be replaced by :meth:`today`.  Compute a date
        using :func:`lino.utils.date_offset` based on the process
        startup time (or :attr:`the_demo_date` if this is set).

        Used in Python fixtures and unit tests.
        """
        base = self.the_demo_date or self.startup_time.date()
        return date_offset(base, *args, **kwargs)

    def today(self, *args, **kwargs):
        """
        Almost the same as :func:`datetime.date.today`.

        One difference is that the system's *today* is replaced by
        :attr:`the_demo_date` if that attribute is set.

        Another difference is that arguments can be passed to add some
        offset. See :func:`atelier.utils.date_offset`.

        This feature is being used in many test cases where e.g. the
        age of people would otherwise change.
        """
        if self.site_config is None:
            base = self.the_demo_date or datetime.date.today()
        else:
            base = self.site_config.simulate_today \
                or self.the_demo_date or datetime.date.today()
        return date_offset(base, *args, **kwargs)

    def welcome_text(self):
        """
        Return the text to display in a console window when this
        application starts.
        """
        return "This is %s using %s." % (self.site_version(),
                                         self.using_text())

    def using_text(self):
        """Return the text to display in a console window when Lino starts.
        """
        return ', '.join(
            [u"%s %s" % (n, v) for n, v, u in self.get_used_libs()])

    def site_version(self):
        """
        Return the name of the application running on this site, including the
        version (if a version is specified).

        Used in footnote or header of certain printed documents."""
        if self.version:
            return self.verbose_name + ' ' + self.version
        return self.verbose_name

    # def configure_plugin(self, app_label, **kw):
    #     raise Exception("Replace SITE.configure_plugin by ad.configure_plugin")

    def install_migrations(self, *args):
        """
        See :func:`lino.utils.dpy.install_migrations`.
        """
        from lino.utils.dpy import install_migrations
        install_migrations(self, *args)

    def parse_date(self, s):
        """
        Convert a string formatted using :attr:`date_format_strftime` or
        :attr:`date_format_extjs` into a `(y,m,d)` tuple (not a
        `datetime.date` instance).  See `/blog/2010/1130`.
        """
        ymd = tuple(reversed(list(map(int, s.split('.')))))
        if len(ymd) != 3:
            raise ValueError(
                "{} is not a valid date (format must be dd.mm.yyyy).".format(
                    s))
        return ymd
        #~ return datetime.date(*ymd)

    def parse_time(self, s):
        """
        Convert a string into a `datetime.time` instance using regex.
        only supports hours and min, not seconds.
        """
        # hms = list(map(int, s.split(':')))
        # return datetime.time(*hms)
        reg = re.compile(
            r"^(\d(?:\d(?=[.,:; ]?\d\d|[.,:; ]\d|$))?)?[.,:; ]?(\d{0,2})$")
        match = reg.match(s)
        if match is None:
            raise ValueError("%s is not a valid time" % s)
        hours, mins = match.groups()
        hours = int(hours) if hours != "" else 0
        mins = int(mins) if mins != "" else 0
        return datetime.time(hour=hours, minute=mins)

    def parse_datetime(self, s):
        """
        Convert a string formatted using :attr:`datetime_format_strftime`
        or :attr:`datetime_format_extjs` into a `datetime.datetime`
        instance.
        """
        #~ print "20110701 parse_datetime(%r)" % s
        #~ s2 = s.split()
        s2 = s.split('T')
        if len(s2) != 2:
            raise Exception("Invalid datetime string %r" % s)
        ymd = list(map(int, s2[0].split('-')))
        hms = list(map(int, s2[1].split(':')))
        return datetime.datetime(*(ymd + hms))
        #~ d = datetime.date(*self.parse_date(s[0]))
        #~ return datetime.combine(d,t)

    def strftime(self, t):
        if t is None:
            return ''
        return t.strftime(self.time_format_strftime)

    def resolve_virtual_fields(self):
        # print("20181023 resolve_virtual_fields()")
        for vf in self.VIRTUAL_FIELDS:
            vf.lino_resolve_type()
        self.VIRTUAL_FIELDS = set()

    def register_virtual_field(self, vf):
        """Call lino_resolve_type after startup."""
        if self._startup_done:
            # raise Exception("20190102")
            vf.lino_resolve_type()
        else:
            # print("20181023 postpone resolve_virtual_fields() for {}".format(vf))
            self.VIRTUAL_FIELDS.add(vf)

    def find_config_file(self, *args, **kwargs):
        return self.confdirs.find_config_file(*args, **kwargs)

    def find_template_config_files(self, *args, **kwargs):
        return self.confdirs.find_template_config_files(*args, **kwargs)

    def setup_actions(self):
        """
        Hook for subclasses to add or modify actions.
        """
        from lino.core.merge import MergeAction
        for m in get_models():
            if m.allow_merge_action:
                m.define_action(merge_row=MergeAction(m))

    def add_user_field(self, name, fld):
        if self.user_model:
            from lino.api import dd
            dd.inject_field(self.user_model, name, fld)

    def get_used_libs(self, html=None):
        """
        Yield a list of (name, version, url) tuples describing the
        third-party software used on this site.

        This function is used by :meth:`using_text` and
        :meth:`welcome_html`.

        """

        import lino
        yield ("Lino", lino.SETUP_INFO['version'], lino.SETUP_INFO['url'])

        try:
            import mod_wsgi
            if getattr(mod_wsgi, "version", None) is None:
                raise ImportError
            version = "{0}.{1}".format(*mod_wsgi.version)
            yield ("mod_wsgi", version, "http://www.modwsgi.org/")
        except ImportError:
            pass

        import django
        yield ("Django", django.get_version(), "http://www.djangoproject.com")

        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python", version, "http://www.python.org/")

        import babel
        yield ("Babel", babel.__version__, "http://babel.edgewall.org/")

        import jinja2
        version = getattr(jinja2, '__version__', '')
        yield ("Jinja", version, "http://jinja.pocoo.org/")

        import dateutil
        version = getattr(dateutil, '__version__', '')
        yield ("python-dateutil", version, "http://labix.org/python-dateutil")

        for p in self.sorted_plugins:
            for u in p.get_used_libs(html):
                yield u

    def get_social_auth_links(self, chunks=False):
        # print("20171207 site.py")
        # elems = []
        if self.social_auth_backends is None or not has_socialauth:
            return
        from social_core.backends.utils import load_backends
        # from collections import OrderedDict
        # from django.conf import settings
        # from social_core.backends.base import BaseAuth
        # backend = module_member(auth_backend)
        # if issubclass(backend, BaseAuth):
        for b in load_backends(self.social_auth_backends).values():
            if chunks:
                yield (b.name, "/oauth/login/" + b.name)  # name, href
            else:
                yield E.a(b.name, href="/oauth/login/" + b.name)
        # print("20171207 a", elems)
        # return E.div(*elems)

    def apply_languages(self):
        """This function is called when a Site object gets instantiated,
        i.e. while Django is still loading the settings. It analyzes
        the :attr:`languages` attribute and converts it to a tuple of
        :data:`LanguageInfo` objects.

        """

        if isinstance(self.languages, tuple) \
           and isinstance(self.languages[0], LanguageInfo):
            # e.g. override_defaults() has been called explicitly, without
            # specifying a languages keyword.
            return

        self.language_dict = dict()  # maps simple_code -> LanguageInfo

        self.LANGUAGE_CHOICES = []
        self.LANGUAGE_DICT = dict()  # used in lino.modlib.users
        must_set_language_code = False

        #~ self.AVAILABLE_LANGUAGES = (to_locale(self.DEFAULT_LANGUAGE),)
        if self.languages is None:
            self.languages = [DJANGO_DEFAULT_LANGUAGE]
            #~ self.update_settings(USE_L10N = False)

            #~ info = LanguageInfo(DJANGO_DEFAULT_LANGUAGE,to_locale(DJANGO_DEFAULT_LANGUAGE),0,'')
            #~ self.DEFAULT_LANGUAGE = info
            #~ self.languages = (info,)
            #~ self.language_dict[info.name] = info
        else:
            if isinstance(self.languages, str):
                self.languages = str(self.languages).split()
            #~ lc = [x for x in self.django_settings.get('LANGUAGES' if x[0] in languages]
            #~ lc = language_choices(*self.languages)
            #~ self.update_settings(LANGUAGES = lc)
            #~ self.update_settings(LANGUAGE_CODE = lc[0][0])
            #~ self.update_settings(LANGUAGE_CODE = self.languages[0])
            # self.update_settings(USE_L10N=True)
            must_set_language_code = True

        languages = []
        for i, django_code in enumerate(self.languages):
            assert_django_code(django_code)
            name = str(to_locale(django_code))
            if name in self.language_dict:
                raise Exception("Duplicate name %s for language code %r" %
                                (name, django_code))
            if i == 0:
                suffix = ''
            else:
                suffix = '_' + name
            info = LanguageInfo(str(django_code), str(name), i, str(suffix))
            self.language_dict[name] = info
            languages.append(info)

        new_languages = languages
        for info in tuple(new_languages):
            if '-' in info.django_code:
                base, loc = info.django_code.split('-')
                if not base in self.language_dict:
                    self.language_dict[base] = info

                    # replace the complicated info by a simplified one
                    #~ newinfo = LanguageInfo(info.django_code,base,info.index,info.suffix)
                    #~ new_languages[info.index] = newinfo
                    #~ del self.language_dict[info.name]
                    #~ self.language_dict[newinfo.name] = newinfo

        #~ for base,lst in simple_codes.items():
        #~ if len(lst) == 1 and and not base in self.language_dict:
        #~ self.language_dict[base] = lst[0]

        self.languages = tuple(new_languages)
        self.DEFAULT_LANGUAGE = self.languages[0]

        self.BABEL_LANGS = tuple(self.languages[1:])

        if must_set_language_code:
            self.update_settings(LANGUAGE_CODE=self.languages[0].django_code)
            # Note: LANGUAGE_CODE is what *Django* believes to be the
            # default language.  This should be some variant of
            # English ('en' or 'en-us') if you use
            # `django.contrib.humanize`
            # https://code.djangoproject.com/ticket/20059

        self.setup_languages()

    def setup_languages(self):
        """
        Reduce Django's :setting:`LANGUAGES` to my `languages`.
        Note that lng.name are not yet translated, we take these
        from `django.conf.global_settings`.
        """

        from django.conf.global_settings import LANGUAGES

        def langtext(code):
            for k, v in LANGUAGES:
                if k == code:
                    return v
            # returns None if not found

        def _add_language(code, lazy_text):
            self.LANGUAGE_DICT[code] = lazy_text
            self.LANGUAGE_CHOICES.append((code, lazy_text))

        if self.languages is None:
            _add_language(DJANGO_DEFAULT_LANGUAGE, _("English"))

        else:

            for lang in self.languages:
                code = lang.django_code
                text = langtext(code)
                if text is None:
                    # Django doesn't know these
                    if code == 'de-be':
                        text = gettext_noop("German (Belgium)")
                    elif code == 'de-ch':
                        text = gettext_noop("German (Swiss)")
                    elif code == 'de-at':
                        text = gettext_noop("German (Austria)")
                    elif code == 'en-us':
                        text = gettext_noop("American English")
                    else:
                        raise Exception(
                            "Unknown language code %r (must be one of %s)" %
                            (lang.django_code, [x[0] for x in LANGUAGES]))

                text = _(text)
                _add_language(lang.django_code, text)
            """
            Cannot activate the site's default language
            because some test cases in django.contrib.humanize
            rely on en-us as default language
            """
            #~ set_language(self.get_default_language())
            """
            reduce Django's LANGUAGES to my babel languages:
            """
            self.update_settings(
                LANGUAGES=[x for x in LANGUAGES if x[0] in self.LANGUAGE_DICT])

    def get_language_info(self, code):
        return self.language_dict.get(code, None)

    def resolve_languages(self, languages):
        rv = []
        if isinstance(languages, str):
            languages = str(languages).split()
        for k in languages:
            if isinstance(k, str):
                li = self.get_language_info(k)
                if li is None:
                    raise Exception(
                        "Unknown language code %r (must be one of %s)" %
                        (str(k), [i.name for i in self.languages]))
                rv.append(li)
            else:
                assert k in self.languages
                rv.append(k)
        return tuple(rv)

    def language_choices(self, language, choices):
        l = choices.get(language, None)
        if l is None:
            l = choices.get(self.DEFAULT_LANGUAGE)
        return l

    def get_default_language(self):
        return self.DEFAULT_LANGUAGE.django_code

    def str2dict(self, txt, **kw):
        for simple, info in self.language_dict.items():
            with translation.override(simple):
                kw[simple] = str(txt)
        return kw

    def str2kw(self, field_name, txt, **kw):
        # from django.utils import translation
        for simple, info in self.language_dict.items():
            with translation.override(simple):
                kw[field_name + info.suffix] = str(txt)
        return kw

    def babelkw(self, name, txt=None, **kw):
        if txt is None:
            d = dict()
        else:
            d = self.str2kw(name, txt)
        for simple, info in self.language_dict.items():
            v = kw.get(simple, None)
            if v is not None:
                d[name + info.suffix] = str(v)
        return d

    def args2kw(self, name, *args):
        assert len(args) == len(self.languages)
        kw = {name: args[0]}
        for i, lang in enumerate(self.BABEL_LANGS):
            kw[name + '_' + lang] = args[i + 1]
        return kw

    def field2kw(self, obj, name, **known_values):
        # d = { self.DEFAULT_LANGUAGE.name : getattr(obj,name) }
        for lng in self.languages:
            v = getattr(obj, name + lng.suffix, None)
            if v:
                known_values[lng.name] = v
        return known_values

    def field2args(self, obj, name):
        return [str(getattr(obj, name + li.suffix)) for li in self.languages]
        #~ l = [ getattr(obj,name) ]
        #~ for lang in self.BABEL_LANGS:
        #~ l.append(getattr(obj,name+'_'+lang))
        #~ return l

    def babelitem(self, *args, **values):
        if len(args) == 0:
            info = self.language_dict.get(get_language(),
                                          self.DEFAULT_LANGUAGE)
            default_value = None
            if info == self.DEFAULT_LANGUAGE:
                return values.get(info.name)
            x = values.get(info.name, None)
            if x is None:
                return values.get(self.DEFAULT_LANGUAGE.name)
            return x
        elif len(args) == 1:
            info = self.language_dict.get(get_language(), None)
            if info is None:
                return args[0]
            default_value = args[0]
            return values.get(info.name, default_value)
        # args = tuple_py2(args)
        # print(type(args))
        raise ValueError("%(values)s is more than 1 default value." %
                         dict(values=args))

    # babel_get(v) = babelitem(**v)

    def babeldict_getitem(self, d, k):
        v = d.get(k, None)
        if v is not None:
            assert type(v) is dict
            return self.babelitem(**v)

    def babelattr(self, obj, attrname, default=NOT_PROVIDED, language=None):
        if language is None:
            language = get_language()
        info = self.language_dict.get(language, self.DEFAULT_LANGUAGE)
        if info.index != 0:
            v = getattr(obj, attrname + info.suffix, None)
            if v:
                return v
        if default is NOT_PROVIDED:
            return getattr(obj, attrname)
        else:
            return getattr(obj, attrname, default)
        #~ if lang is not None and lang != self.DEFAULT_LANGUAGE:
        #~ v = getattr(obj,attrname+"_"+lang,None)
        #~ if v:
        #~ return v
        #~ return getattr(obj,attrname,*args)

    def diagnostic_report_rst(self, *args):
        """Returns a string with a diagnostic report about this
site. :manage:`diag` is a command-line shortcut to this.

        """
        s = ''
        s += rstgen.header(1, "Plugins")
        for n, p in enumerate(self.installed_plugins):
            s += "%d. " % (n + 1)
            s += "{} : {}\n".format(p.app_label, p)
        # s += "config_dirs: %s\n" % repr(self.confdirs.config_dirs)
        s += "\n"
        s += rstgen.header(1, "Config directories")
        for n, cd in enumerate(self.confdirs.config_dirs):
            s += "%d. " % (n + 1)
            ln = relpath(cd.name)
            if cd.writeable:
                ln += " [writeable]"
            s += ln + '\n'
        # for arg in args:
        #     p = self.plugins[arg]
        return s

    # def get_db_overview_rst(self):
    #     from lino.utils.diag import analyzer
    #     analyzer.show_db_overview()

    def override_defaults(self, **kwargs):
        self.override_settings(**kwargs)
        self.install_settings()

    def is_imported_partner(self, obj):
        """
        Return whether the specified
        :class:`Partner <ml.contacts.Partner>` instance
        `obj` is to be considered as imported from some legacy database.
        """
        #~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
        return False
        #~ return obj.id is not None and (obj.id > 10 and obj.id < 21)

    def site_header(self):
        """Used in footnote or header of certain printed documents.

        The convention is to call it as follows from an appy.pod template
        (use the `html` function, not `xhtml`)
        ::

          do text
          from html(settings.SITE.site_header())

        Note that this is expected to return a unicode string possibly
        containing valid HTML (not XHTML) tags for formatting.

        """
        if self.is_installed('contacts') and self.site_config:
            if self.site_config.site_company:
                return self.site_config.site_company.get_address('<br/>')
                #~ s = unicode(self.site_config.site_company) + " / "  + s
        #~ return ''

    # def setup_main_menu(self):
    #     """
    #     To be implemented by applications.
    #     """
    #     pass

    def get_dashboard_items(self, user):
        """Expected to yield a sequence of items to be rendered on the
        dashboard (:xfile:`admin_main.html`).

        The default implementation calls :meth:`get_dashboard_items
        <lino.core.plugin.Plugin.get_dashboard_items>` on every
        installed plugin and yields all items.

        The items will be rendered in that order, except if
        :mod:`lino.modlib.dashboard` is installed to enable per-user
        customized dashboard.

        """
        if user:
            for p in self.installed_plugins:
                for i in p.get_dashboard_items(user):
                    yield i

    @property
    def site_config(self):
        """
        This property holds a cached version of the one and only
        :class:`SiteConfig <lino.modlib.system.SiteConfig>` row
        that holds site-wide database-stored and web-editable Site
        configuration parameters.

        If no instance exists (which happens in a virgin database), we create it
        using default values from :attr:`site_config_defaults`.

        This is `None` when :mod:`lino.modlib.system` is not installed.

        It can also be `None` when startup is not done,  which can happen e.g.
        on an asgi web server.

        """
        if 'system' not in self.models:
            return None

        return self.models.system.SiteConfig.get_site_config()

    #~ site_config = property(get_site_config)

    #~ def shutdown(self):
    #~ self.clear_site_config()
    #~ return super(Site,self).shutdown()

    def clear_site_config(self):
        """
        Clear the cached SiteConfig instance.

        This is needed e.g. when the test runner has created a new
        test database.
        """
        # from lino.core.utils import obj2str
        # print("20180502 clear_site_config {}".format(
        #     obj2str(self._site_config, True)))
        if 'system' in self.models:
            self.models.system.SiteConfig.clear_site_config()

    @property
    def quicklinks(self):
        """The list of `quick links`.

        This is lazily created when first accessed.

        """
        if self._quicklinks is None:
            from lino.core.menus import QuickLinksList
            qll = QuickLinksList()
            for ql in self.get_quicklinks():
                qll.add_action(ql)
            self.setup_quicklinks(None, qll)
            self._quicklinks = qll
        return self._quicklinks

    def get_quicklink_items(self, user_type):
        """Yield the quick links that are visible for the given user type.

        """
        for ql in self.quicklinks.items:
            if ql.bound_action.get_view_permission(user_type):
                yield ql

    def get_quicklinks_html(self, ar, user):
        qll = []
        for ql in self.get_quicklink_items(user.user_type):
            if ql.bound_action.get_bound_action_permission(ar):
                qll.append(tostring(ar.menu_item_button(ql)))

        # if getattr(ar.renderer.front_end, 'autorefresh_seconds', 0) > 0:
        #     qll.append(
        #         '<a href="javascript:Lino.autorefresh();">autorefresh</a>')
        # if False:
        #     qll.append(
        #         '<a href="javascript:{}" style="text-decoration:none">{}</a>'.
        #         format(self.kernel.default_renderer.reload_js(), _("Refresh")))

        return " | ".join(qll)

    def get_quicklinks(self):
        """
        Return or yield a sequence of quick link descriptors to be added to the
        list of quick links.

        Override this to define application-specific quick links.
        """
        return []

    def setup_quicklinks(self, unused, tb):
        """
        Customize the list of :term:`quick links <quick link>`.
        Override this to define application-specific quick links.

        Default implementation calls :meth:`get_quicklinks
        <lino.core.plugins.Plugin.get_quicklinks>` and :meth:`setup_quicklinks
        <lino.core.plugins.Plugin.setup_quicklinks>` for each installed plugin.

        The quicklinks yielded by :meth:`get_quicklinks
        <lino.core.plugins.Plugin.get_quicklinks>` will be added before
        calling :meth:`setup_quicklinks
        <lino.core.plugins.Plugin.setup_quicklinks>`.

        """
        for p in self.sorted_plugins:
            p.setup_quicklinks(tb)
            for spec in p.get_quicklinks():
                tb.add_action(spec)

    def get_site_menu(self, user_type):
        """
        Return this site's main menu for the given UserType.
        Must be a :class:`lino.core.menus.Toolbar` instance.
        Applications usually should not need to override this.
        """
        from lino.core import menus
        main = menus.Toolbar(user_type, 'main')
        self.setup_menu(user_type, main)
        main.compress()
        return main

    _sorted_plugins = None

    @property
    def sorted_plugins(self):
        # change the "technical" plugin order into the order visible to the end
        # user.  The end user wants to see menu entries of explicitly installed
        # plugins before those of automatically installed plugins.
        if self._sorted_plugins is None:
            self._sorted_plugins = []
            for p in self.installed_plugins:
                if not p.is_hidden() and p.needed_by is None:
                    # explicitly installed
                    self._sorted_plugins.append(p)
            for p in self.installed_plugins:
                if not p.is_hidden() and p.needed_by is not None:
                    # automatically installed
                    self._sorted_plugins.append(p)
        return self._sorted_plugins

    def setup_menu(self, user_type, main):
        """Set up the application's menu structure.

        See :doc:`/dev/menu` and :doc:`/dev/xlmenu`.

        """
        # from django.apps import apps
        # apps = [a.models_module for a in apps.get_app_configs()]

        for k, label in self.top_level_menus:
            methname = "setup_{0}_menu".format(k)

            #             for mod in apps:
            #                 if hasattr(mod, methname):
            #                     msg = "{0} still has a function {1}(). \
            # Please convert to Plugin method".format(mod, methname)
            #                     raise ChangedAPI(msg)

            if label is None:
                menu = main
            else:
                menu = main.add_menu(k, label)
            for p in self.sorted_plugins:
                meth = getattr(p, methname, None)
                if meth is not None:
                    meth(self, user_type, menu)
                    # print("20190430 {} {} ({}) --> {}".format(
                    #       k, p.app_label, p.needed_by, [i.name for i in main.items]))

    def get_middleware_classes(self):
        """Yields the strings to be stored in
        the :setting:`MIDDLEWARE_CLASSES` setting.

        In case you don't want to use this method for defining
        :setting:`MIDDLEWARE_CLASSES`, you can simply set
        :setting:`MIDDLEWARE_CLASSES` in your :xfile:`settings.py`
        after the :class:`Site` has been instantiated.

        `Django and standard HTTP authentication
        <https://stackoverflow.com/questions/152248/can-i-use-http-basic-authentication-with-django>`_

        """

        yield 'django.middleware.common.CommonMiddleware'
        if self.languages and len(self.languages) > 1:
            yield 'django.middleware.locale.LocaleMiddleware'

        if self.user_model:
            yield 'django.contrib.sessions.middleware.SessionMiddleware'
            # yield 'django.contrib.auth.middleware.AuthenticationMiddleware'
            yield 'lino.core.auth.middleware.AuthenticationMiddleware'
            yield 'lino.core.auth.middleware.WithUserMiddleware'
            # yield 'lino.core.auth.middleware.DeviceTypeMiddleware'
        else:
            yield 'lino.core.auth.middleware.NoUserMiddleware'

        if self.get_auth_method() == 'remote':
            # yield 'django.contrib.auth.middleware.RemoteUserMiddleware'
            yield 'lino.core.auth.middleware.RemoteUserMiddleware'
        # if self.use_ipdict:
        #     yield 'lino.modlib.ipdict.middleware.Middleware'
        if has_socialauth and self.get_plugin_setting(
                'users', 'third_party_authentication', False):
            yield 'social_django.middleware.SocialAuthExceptionMiddleware'

        if True:
            yield 'lino.utils.ajax.AjaxExceptionResponse'

        if self.use_security_features:
            yield 'django.middleware.security.SecurityMiddleware'
            yield 'django.middleware.clickjacking.XFrameOptionsMiddleware'
            # yield 'django.middleware.csrf.CsrfViewMiddleware'

        if False:
            #~ yield 'lino.utils.sqllog.ShortSQLLogToConsoleMiddleware'
            yield 'lino.utils.sqllog.SQLLogToConsoleMiddleware'
            #~ yield 'lino.utils.sqllog.SQLLogMiddleware'

    # def get_main_action(self, user_type):
    #     """No longer used.
    #     Return the action to show as top-level "index.html".
    #     The default implementation returns `None`, which means
    #     that Lino will call :meth:`get_main_html`.
    #     """
    #     return None

    def __deepcopy__(self):
        raise Exception("Who is copying me?!")

    def __copy__(self):
        raise Exception("Who is copying me?!")

    def get_main_html(self, ar, **context):
        """Return a chunk of html to be displayed in the main area of the
        admin index.  This is being called only if
        :meth:`get_main_action` returns `None`.  The default
        implementation renders the :xfile:`admin_main.html` template.

        """
        # assert request is not None
        # print("20210615 get_main_html()", ar)
        # if front_end is None:
        #     front_end = self.kernel.default_ui
        return self.plugins.jinja.render_from_ar(ar, 'admin_main.html',
                                                 **context)

    def build_site_cache(self, force=False, later=False, verbosity=1):
        """
        Populate the :term:`site cache`, especially the
        :xfile:`lino*.js` files, one per user :term:`user type` and language.

        - ``force``: rebuild the files even if they are up to date

        - ``later``: don't rebuild now, just touch the :xfile:`settings.py` so
          that they get rebuild next time.

        """
        # if not self.is_prepared:
        #     self.prepare_layouts()
        #     self.is_prepared = True

        if later:
            settings_file = self.django_settings.get("__file__")
            Path(settings_file).touch()
            # print("20230823 later")
            return

        if self.never_build_site_cache:
            self.logger.debug(
                "Not building site cache because `settings.SITE.never_build_site_cache` is True"
            )
            # print("20230823 never")
            return

        # logger.info("20140401 build_site_cache started")

        if not self.media_root.is_dir():
            self.media_root.mkdir()
            # try:
            #     settings.SITE.media_root.mkdir()
            # except Exception as e:
            #     logger.debug(
            #         "Not building site cache because 'mkdir %s' says %s.",
            #         settings.SITE.media_root, e)
            #     return

        self.makedirs_if_missing(self.media_root / 'webdav')

        from lino.modlib.users.utils import with_user_profile
        from lino.modlib.users.choicelists import UserTypes
        # from django.utils import translation

        started = time.time()
        count = 0
        # rnd = self.kernel.default_ui.renderer
        # renderers = [p.renderer for p in self.installed_plugins if p.renderer is not None]
        for lng in self.languages:
            with translation.override(lng.django_code):
                for user_type in UserTypes.objects():
                    if verbosity > 0:
                        self.logger.info("Build JS cache for %s (%s).",
                                         user_type, lng.name)
                    for wf in self.kernel.web_front_ends:
                        count += with_user_profile(user_type,
                                                   wf.renderer.build_js_cache,
                                                   force, verbosity)
        if verbosity > 0:
            self.logger.info(
                "%d lino*.js files have been built in %s seconds.", count,
                time.time() - started)

    def get_welcome_messages(self, ar):
        """
        Yields a list of "welcome messages" (see
        :meth:`lino.core.actors.Actor.get_welcome_messages`) of all
        actors.  This is being called from :xfile:`admin_main.html`.
        """

        for h in self._welcome_handlers:
            for msg in h(ar):
                yield msg
        # for a in self._welcome_actors:
        #     for msg in a.get_welcome_messages(ar):
        #         yield msg

    def add_welcome_handler(self, func, actor=None, msg=None):
        """
        Add the given callable as a "welcome handler".  Lino will call
        every welcome handler for every incoming request, passing them
        a :class:`BaseRequest <lino.core.requests.BaseRequest>`
        instance representing this request as positional argument.
        The callable is expected to yield a series of messages
        (usually either 0 or 1). Each message must be either a string
        or a :class:`E.span <etgen.html.E>` element.
        """
        # print(
        #     "20161219 add_welcome_handler {} {} {}".format(
        #         actor, msg, func))
        self._welcome_handlers.append(func)

    def setup_features(self):

        def add_features(app_name):
            if isinstance(app_name, str):
                m = import_module(app_name)
                if not hasattr(m, 'Plugin'):
                    return
                p = getattr(m, 'Plugin')
                p.setup_site_features(self)
            else:
                for app in app_name:
                    add_features(app)

        for app in self.get_installed_apps():
            add_features(app)

    def get_installed_apps(self):
        if self.django_admin_prefix:
            yield 'django.contrib.admin'  # not tested

        yield 'django.contrib.staticfiles'
        yield 'lino.modlib.about'

        if self.use_ipdict:
            yield 'lino.modlib.ipdict'

        if isinstance(self.social_auth_backends, list) and len(
                self.social_auth_backends) == 0:
            raise Exception(
                "Incorrect value for social_auth_backends,"
                "social_auth_backends should be None or non-empty list.")

        if self.default_ui is not None:
            yield self.default_ui
        if self.web_front_ends is not None:
            for prefix, modname in self.web_front_ends:
                yield modname

        # if self.admin_ui is not None:
        #     if self.admin_ui == self.default_ui:
        #         raise Exception(
        #             "admin_ui (if specified) must be different "
        #             "from default_ui")
        #     yield self.admin_ui

        # if self.use_linod:
        #     yield 'lino.modlib.linod'

        # if self.default_ui == "extjs":
        #     yield 'lino.modlib.extjs'
        #     yield 'lino.modlib.bootstrap3'
        # elif self.default_ui == "bootstrap3":
        #     yield 'lino.modlib.bootstrap3'

        # yield "lino.modlib.lino_startup"

    # server_url = None
    copyright_name = None
    """Name of copyright holder of the site's content."""

    copyright_url = None

    server_url = "http://127.0.0.1:8000/"
    """The "official" URL used by "normal" users when accessing this Lino
    site.

    This is used by templates such as :xfile:`summary.eml` (used by
    :mod:`lino.modlib.notify` to send notification emails)

    Django has a `HttpRequest.build_absolute_uri()
    <https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpRequest.build_absolute_uri>`__
    method, but e.g. notification emails are sent via :manage:`linod` where no
    HttpRequest exists. That's why we need to manually set :attr:`server_url`.

    """

    site_prefix = '/'
    """The string to prefix to every URL of the Lino web interface.

    This must *start and end with a *slash*.  Default value is
    ``'/'``.

    This must be set if your project is not being served at the "root"
    URL of your server.

    If this is different from the default value, Lino also sets
    :setting:`SESSION_COOKIE_PATH`.

    When this Site is running under something else than a development
    server, this setting must correspond to your web server's
    configuration.  For example if you have::

        WSGIScriptAlias /foo /home/luc/mypy/lino_sites/foo/wsgi.py

    Then your :xfile:`settings.py` should specify::

        site_prefix = '/foo/'

    See also :ref:`mass_hosting`.

    """

    # def urlkwargs(self, **kw):
    #     """
    #
    #     Return the current url preferences as a dict to pass to buildurl in
    #     order to forward them to a next url.
    #
    #     """
    #     lng = get_language()
    #     if len(self.languages) > 1 and self.DEFAULT_LANGUAGE.django_code != lng:
    #         kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lng)
    #     return kw

    def buildurl(self, *args, **kw):
        return buildurl(self.site_prefix, *args, **kw)

    def build_media_url(self, *args, **kw):
        return buildurl(settings.MEDIA_URL, *args, **kw)

    def build_static_url(self, *args, **kw):
        return buildurl(settings.STATIC_URL, *args, **kw)

    def build_site_cache_url(self, *args, **kw):
        assert str(self.media_root) == str(settings.MEDIA_ROOT)
        # if str(self.media_root) != str(settings.MEDIA_ROOT):
        #     return self.build_static_url(*args, **kw)
        return self.build_media_url(*args, **kw)

    def welcome_html(self, ui=None):
        """
        Return a HTML version of the "This is APPLICATION
        version VERSION using ..." text. to be displayed in the
        About dialog, in the plain html footer, and maybe at other
        places.

        """
        from django.utils.translation import gettext as _

        p = []
        sep = ''
        if self.verbose_name:
            p.append(_("This website runs "))
            if self.url:
                p.append(
                    E.a(str(self.verbose_name), href=self.url,
                        target='_blank'))
            else:
                p.append(E.b(str(self.verbose_name)))
            if self.version:
                p.append(' ')
                p.append(self.version)
            sep = _(' using ')

        for name, version, url in self.get_used_libs(html=E):
            p.append(sep)
            p.append(E.a(name, href=url, target='_blank'))
            p.append(' ')
            p.append(version)
            sep = ', '

        yield E.span(*p)

    def login(self, username=None, **kw):
        """Open a session as the user with the given `username`.

        For usage from a shell or a tested document.  Does not require
        any password because when somebody has command-line access we
        trust that she has already authenticated.

        It returns a
        :class:`BaseRequest <lino.core.requests.BaseRequest>` object.

        """
        from lino.core import requests
        self.startup()
        User = self.user_model
        if User and username:
            try:
                kw.update(user=User.objects.get(username=username))
            except User.DoesNotExist:
                raise User.DoesNotExist(
                    "'{0}' : no such user".format(username))

        # if not 'renderer' in kw:
        #     kw.update(renderer=self.ui.text_renderer)

        # import lino.core.urls  # hack: trigger ui instantiation
        return requests.BaseRequest(**kw)

    def get_letter_date_text(self, today=None):
        """
        Returns a string like "Eupen, den 26. August 2013".
        """
        sc = self.site_config.site_company
        if today is None:
            today = self.today()
        from lino.utils.format_date import fdl
        if sc and sc.city:
            return _("%(place)s, %(date)s") % dict(place=str(sc.city.name),
                                                   date=fdl(today))
        return fdl(today)

    def decfmt(self, v, places=2, **kw):
        """
        Format a Decimal value using :func:`lino.utils.moneyfmt`, but
        applying the site settings
        :attr:`lino.Lino.decimal_group_separator` and
        :attr:`lino.Lino.decimal_separator`.

        """
        kw.setdefault('sep', self.decimal_group_separator)
        kw.setdefault('dp', self.decimal_separator)
        from lino.utils import moneyfmt
        if v is None:
            return ""
        return moneyfmt(v, places=places, **kw)

    def format_currency(self, *args, **kwargs):
        """
        Return the given number as a string formatted according to the
        :attr:`site_locale` setting on this site.

        All arguments are forwarded to `locale.locale()
        <https://docs.python.org/3/library/locale.html#locale.currency>`__.
        """
        res = locale.currency(*args, **kwargs)
        # if six.PY2:
        #     res = res.decode(locale.nl_langinfo(locale.CODESET))
        return res

    LOOKUP_OP = '__iexact'

    def lookup_filter(self, fieldname, value, **kw):
        """
        Return a `models.Q` to be used if you want to search for a given
        string in any of the languages for the given babel field.
        """
        from django.db.models import Q
        kw[fieldname + self.LOOKUP_OP] = value
        #~ kw[fieldname] = value
        flt = Q(**kw)
        del kw[fieldname + self.LOOKUP_OP]
        for lng in self.BABEL_LANGS:
            kw[fieldname + lng.suffix + self.LOOKUP_OP] = value
            flt = flt | Q(**kw)
            del kw[fieldname + lng.suffix + self.LOOKUP_OP]
        return flt

    # def relpath(self, p):
    #     """Used by :class:`lino.mixins.printable.EditTemplate` in order to
    #     write a testable message...

    #     """
    #     if p.startswith(self.project_dir):
    #         p = "$(PRJ)" + p[len(self.project_dir):]
    #     return p

    def resolve_plugin(self, app_label):
        return self.plugins.get(app_label, None)

    def get_plugin_setting(self, plugin_name, option_name, *default):
        """
        Return the given plugin setting if the plugin is installed, otherwise
        the provided default value.
        """
        if self.installed_plugin_modules is None:
            p = PLUGIN_CONFIGS.get(plugin_name, {})
            return p.get(option_name, *default)
        if self.is_installed(plugin_name):
            p = self.plugins.get(plugin_name)
            return getattr(p, option_name, *default)
        if len(default) == 0:
            raise Exception(
                "Plugin {} is not installed and no default was provided".
                format(plugin_name))
        return default[0]


class TestSite(Site):
    """Used to simplify doctest strings because it inserts default values
    for the two first arguments that are mandatory but not used in our
    examples.

    Example::

    >> from lino.core.site import Site
    >> Site(globals(), ...)

    >> from lino.core.site import TestSite as Site
    >> Site(...)

    """

    def __init__(self, *args, **kwargs):
        # kwargs.update(no_local=True)
        g = dict(__file__=__file__)
        g.update(SECRET_KEY="20227")  # see :djangoticket:`20227`
        super(TestSite, self).__init__(g, *args, **kwargs)

        # 20140913 Hack needed for doctests in :mod:`ad`.
        # from django.utils import translation
        translation._default = None
