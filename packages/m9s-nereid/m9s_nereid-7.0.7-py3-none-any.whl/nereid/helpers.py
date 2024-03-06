# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import os
import time
import warnings

from functools import wraps
from hashlib import md5

import flask.helpers

from flask.helpers import flash as _flash  # noqa
from flask.helpers import url_for as flask_url_for
from flask_login import login_required  # noqa
from speaklater import is_lazy_string
from werkzeug.utils import redirect

import trytond.modules

from trytond import backend
from trytond.config import config
from trytond.tools.misc import slugify as _slugify
from trytond.transaction import Transaction, TransactionError

from .globals import (  # noqa
    current_app, current_locale, current_user, current_website, request)

DATABASE_PATH = config.get('database', 'path')


def url_for(endpoint, **values):
    """
    Generates a URL to the given endpoint with the method provided.
    The endpoint is relative to the active module if modules are in use.

    The functionality is documented in `flask.helpers.url_for`

    In addition to the arguments provided by flask, nereid allows the locale
    of the url to be generated to be specified using the locale attribute.
    The default value of locale is the locale of the current request.

    For example::

        url_for('nereid.website.home', locale='us')

    """
    if 'language' in values:
        warnings.warn(
            "language argument is deprecated in favor of locale",
            DeprecationWarning, stacklevel=2
        )

    # 'static' is Flask's default endpoint for static files.
    # There is no need to set language in URL for static files
    if endpoint != 'static' and \
            'locale' not in values and current_website.locales:
        values['locale'] = current_locale.code

    return flask_url_for(endpoint, **values)


def secure(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not request.is_secure:
            return redirect(request.url.replace('http://', 'https://'))
        else:
            return function(*args, **kwargs)
    return decorated_function


def _prepare_send_file_kwargs(**kwargs):
    # According to werkzeug code '_root_path' should not be used
    # if kwargs.get("_root_path") is None:
    #     kwargs["_root_path"] = os.path.join(
    #         DATABASE_PATH, current_app.database_name)

    path_or_file = kwargs.get("path_or_file")
    if (isinstance(path_or_file, (os.PathLike, str))
            or hasattr(path_or_file, "__fspath__")):
        path_or_file = os.fspath(path_or_file)
        if not os.path.isabs(path_or_file):
            path_or_file = os.path.join(
                DATABASE_PATH, current_app.database_name, path_or_file)

    kwargs.update(
        path_or_file=path_or_file,
    )
    return kwargs


def send_file(
        path_or_file,
        mimetype=None,
        as_attachment=False,
        download_name=None,
        conditional=True,
        etag=True,
        last_modified=None,
        max_age=None,
        ):
    """Send the contents of a file to the client.

    The first argument can be a file path or a file-like object. Paths
    are preferred in most cases because Werkzeug can manage the file and
    get extra information from the path. Passing a file-like object
    requires that the file is opened in binary mode, and is mostly
    useful when building a file in memory with :class:`io.BytesIO`.

    Never pass file paths provided by a user. The path is assumed to be
    trusted, so a user could craft a path to access a file you didn't
    intend. Use :func:`send_from_directory` to safely serve
    user-requested paths from within a directory.

    If the WSGI server sets a ``file_wrapper`` in ``environ``, it is
    used, otherwise Werkzeug's built-in wrapper is used. Alternatively,
    if the HTTP server supports ``X-Sendfile``, configuring Flask with
    ``USE_X_SENDFILE = True`` will tell the server to send the given
    path, which is much more efficient than reading it in Python.

    :param path_or_file: The path to the file to send, relative to the
        current working directory if a relative path is given.
        Alternatively, a file-like object opened in binary mode. Make
        sure the file pointer is seeked to the start of the data.
    :param mimetype: The MIME type to send for the file. If not
        provided, it will try to detect it from the file name.
    :param as_attachment: Indicate to a browser that it should offer to
        save the file instead of displaying it.
    :param download_name: The default name browsers will use when saving
        the file. Defaults to the passed file name.
    :param conditional: Enable conditional and range responses based on
        request headers. Requires passing a file path and ``environ``.
    :param etag: Calculate an ETag for the file, which requires passing
        a file path. Can also be a string to use instead.
    :param last_modified: The last modified time to send for the file,
        in seconds. If not provided, it will try to detect it from the
        file path.
    :param max_age: How long the client should cache the file, in
        seconds. If set, ``Cache-Control`` will be ``public``, otherwise
        it will be ``no-cache`` to prefer conditional caching.

    .. versionchanged:: 2.0
        ``download_name`` replaces the ``attachment_filename``
        parameter. If ``as_attachment=False``, it is passed with
        ``Content-Disposition: inline`` instead.

    .. versionchanged:: 2.0
        ``max_age`` replaces the ``cache_timeout`` parameter.
        ``conditional`` is enabled and ``max_age`` is not set by
        default.

    .. versionchanged:: 2.0
        ``etag`` replaces the ``add_etags`` parameter. It can be a
        string to use instead of generating one.

    .. versionchanged:: 2.0
        Passing a file-like object that inherits from
        :class:`~io.TextIOBase` will raise a :exc:`ValueError` rather
        than sending an empty file.

    .. versionadded:: 2.0
        Moved the implementation to Werkzeug. This is now a wrapper to
        pass some Flask-specific arguments.

    .. versionchanged:: 1.1
        ``filename`` may be a :class:`~os.PathLike` object.

    .. versionchanged:: 1.1
        Passing a :class:`~io.BytesIO` object supports range requests.

    .. versionchanged:: 1.0.3
        Filenames are encoded with ASCII instead of Latin-1 for broader
        compatibility with WSGI servers.

    .. versionchanged:: 1.0
        UTF-8 filenames as specified in :rfc:`2231` are supported.

    .. versionchanged:: 0.12
        The filename is no longer automatically inferred from file
        objects. If you want to use automatic MIME and etag support,
        pass a filename via ``filename_or_fp`` or
        ``attachment_filename``.

    .. versionchanged:: 0.12
        ``attachment_filename`` is preferred over ``filename`` for MIME
        detection.

    .. versionchanged:: 0.9
        ``cache_timeout`` defaults to
        :meth:`Flask.get_send_file_max_age`.

    .. versionchanged:: 0.7
        MIME guessing and etag support for file-like objects was
        removed because it was unreliable. Pass a filename if you are
        able to, otherwise attach an etag yourself.

    .. versionchanged:: 0.5
        The ``add_etags``, ``cache_timeout`` and ``conditional``
        parameters were added. The default behavior is to add etags.

    .. versionadded:: 0.2
    """
    rv = flask.helpers.send_file(
        **_prepare_send_file_kwargs(
            path_or_file=path_or_file,
            mimetype=mimetype,
            as_attachment=as_attachment,
            download_name=download_name,
            conditional=conditional,
            etag=etag,
            last_modified=last_modified,
            max_age=max_age,
        )
    )
    if etag:
        rv.set_etag('nereid-%s' % rv.get_etag()[0])
    return rv


def send_from_directory(
        directory,
        path,
        **kwargs):
    """Send a file from within a directory using :func:`send_file`.

    .. code-block:: python

        @app.route("/uploads/<path:name>")
        def download_file(name):
            return send_from_directory(
                app.config['UPLOAD_FOLDER'], name, as_attachment=True
            )

    This is a secure way to serve files from a folder, such as static
    files or uploads. Uses :func:`~werkzeug.security.safe_join` to
    ensure the path coming from the client is not maliciously crafted to
    point outside the specified directory.

    If the final path does not point to an existing regular file,
    raises a 404 :exc:`~werkzeug.exceptions.NotFound` error.

    :param directory: The directory that ``path`` must be located under,
        relative to the current application's root path.
    :param path: The path to the file to send, relative to
        ``directory``.
    :param kwargs: Arguments to pass to :func:`send_file`.

    .. versionchanged:: 2.0
        ``path`` replaces the ``filename`` parameter.

    .. versionadded:: 2.0
        Moved the implementation to Werkzeug. This is now a wrapper to
        pass some Flask-specific arguments.

    .. versionadded:: 0.5
    """
    return flask.helpers.send_from_directory(
        directory, path, **_prepare_send_file_kwargs(**kwargs)
    )


def slugify(value, hyphenate='-'):
    '''

    .. versionchanged:: 6.0.8
        The slugify method from nereid went partly into Tryton 5.4
        Nereid now uses this method and extends it to return lower
        case on slugs.

    '''
    return _slugify(value, hyphenate=hyphenate).lower()


def _rst_to_html_filter(value):
    """
    Converts RST text to HTML
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    This uses docutils, if the library is missing, then the
    original text is returned

    Loading to environment::
             from jinja2 import Environment
             env = Environment()
             env.filters['rst'] = rst_to_html
             template = env.from_string("Welcome {{name|rst}}")
             template.render(name="**Sharoon**")
    """
    try:
        from docutils import core
        parts = core.publish_parts(source=value, writer_name='html')
        return parts['body_pre_docinfo'] + parts['fragment']
    except Exception:
        return value


def key_from_list(list_of_args):
    """
    Builds a key from a list of arguments which could be used for caching
    The key s constructed as an md5 hash
    """
    hash = md5()
    hash.update(repr(list_of_args).encode('utf-8'))
    return hash.hexdigest()


def get_website_from_host(http_host):
    """Try to find the website name from the HTTP_HOST name"""
    return http_host.split(':')[0]


def make_crumbs(browse_record, endpoint, add_home=True, max_depth=10,
                field_map_changes=None, root_ids=None):
    """
    Makes bread crumbs for a given browse record based on the field
    parent of the browse record

    :param browse_record: The browse record of the object from which upward
                          tracing of crumbs need to be done
    :param endpoint: The endpoint against which the urls have to be generated
    :param add_home: If provided will add home and home url as the first item
    :param max_depth: Maximum depth of the crumbs
    :param field_map_changes: A dictionary/list of key value pair (tuples) to
                              update the default field_map. Only the changing
                              entries need to be provided.
    :param root_ids: IDs of root nodes where the recursion to a parent node
                     will need to be stopped. If not specified the recursion
                     continues upto the max_depth. Expects a list or tuple of
                     ids.

    .. versionchanged:: 0.3
        Added root_ids
    """
    field_map = dict(
        parent_field='parent',
        uri_field='uri',
        title_field='title',
    )
    if field_map_changes is not None:
        field_map.update(field_map_changes)
    if root_ids is None:
        root_ids = tuple()

    def recurse(node, level=1):
        if level > max_depth or not node:
            return []
        data_pair = (
            url_for(endpoint, uri=getattr(node, field_map['uri_field'])),
            getattr(node, field_map['title_field'])
        )
        if node.id in root_ids:
            return [data_pair]
        else:
            return [data_pair] + recurse(
                getattr(node, field_map['parent_field']), level + 1
            )

    items = recurse(browse_record)

    if add_home:
        items.append((url_for('nereid.website.home'), 'Home'))

    # The bread crumb is now in reverse order with home at end, reverse it
    items.reverse()

    return items


def root_transaction(function):
    """
    Decorator to run a function inside a simple Tryton transaction.
    - as root (user 0)
    - readonly transaction
    - no task running
    """
    @wraps(function)
    def decorated_function(self, *args, **kwargs):
        transaction = None
        # Check for existent transaction (needed in test cases)
        if Transaction().connection is None:
            transaction = Transaction().start(
                self.database_name, 0, readonly=True)
        try:
            return function(self, *args, **kwargs)
        finally:
            if transaction is not None:
                transaction.stop()
    return decorated_function


def flash(message, category='message'):
    """
    Lazy strings are no real strings so pickling them results in strange issues.
    Pickling cannot be avoided because of the way sessions work. Hence, this
    special flash function converts lazy strings to unicode content.

    .. versionadded:: 3.0.4.1

    :param message: the message to be flashed.
    :param category: the category for the message.  The following values
                     are recommended: ``'message'`` for any kind of message,
                     ``'error'`` for errors, ``'info'`` for information
                     messages and ``'warning'`` for warnings.  However any
                     kind of string can be used as category.
    """
    if is_lazy_string(message):
        message = str(message)
    return _flash(message, category)


def route(rule, **options):
    """Like :meth:`Flask.route` but for nereid.

    .. versionadded:: 3.0.7.0

    Unlike the implementation in flask and flask.blueprint route decorator does
    not require an existing nereid application or a blueprint instance. Instead
    the decorator adds an attribute to the method called `_url_rules`.

    .. code-block:: python
        :emphasize-lines: 1,7

        from nereid import route

        class Product:
            __name__ = 'product.product'

            @classmethod
            @route('/product/<uri>')
            def render_product(cls, uri):
                ...
                return 'Product Information'

    """
    def decorator(f):
        if not hasattr(f, '_url_rules'):
            f._url_rules = []
        f._url_rules.append((rule, options))
        return f
    return decorator


def get_version():
    """
    Return the version of nereid by looking up the version as read by the
    tryton module loader.
    """
    return trytond.modules.get_module_info('nereid')['version']


def context_processor(name=None):
    """Makes method available in template context. By default method will be
    registered by its name.

    Decorator adds an attribute to the method called `_context_processor`.

    .. code-block:: python
        :emphasize-lines: 1,7

        from nereid import context_processor

        class Product:
            __name__ = 'product.product'

            @classmethod
            @context_processor('get_sale_price')
            def get_sale_price(cls):
                ...
                return 'Product sale price'
    """
    def decorator(f):
        f._context_processor = True
        if name is not None:
            f.__name__ = name
        return f
    return decorator


def template_filter(name=None):
    """
    If you want to register your own filters in Jinja2 you have two ways to do
    that. You can either put them by hand into the jinja_env of the application
    or use the template_filter() decorator.

    The two following examples work the same and both reverse an object::

        from nereid import template_filter

        class MyModel:
            __name__ = 'product.product'

            @classmethod
            @template_filter('reverse')
            def reverse_filter(cls, s):
                return s[::-1]

    Alternatively you can inject it into the jinja environment in your
    `application.py`::

        def reverse_filter(s):
            return s[::-1]
        app.jinja_env.filters['reverse'] = reverse_filter

    In case of the decorator the argument is optional if you want to use the
    function name as name of the filter. Once registered, you can use the
    filter in your templates in the same way as Jinja2’s builtin filters, for
    example if you have a Python list in context called mylist::

        {% for x in mylist | reverse %}
        {% endfor %}
    """
    def decorator(f):
        f._template_filter = True
        if name is not None:
            f.__name__ = name
        return f
    return decorator
