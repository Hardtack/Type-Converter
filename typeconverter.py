# -*- encoding: utf-8 -*-
""":mod:`typeconverter`
~~~~~~~~~~~~~~~~~~~~~~~~

Converts object into specified type.

"""
from __future__ import unicode_literals

from functools import wraps

__version__ = '0.1.0'
__license__ = 'MIT License'
__author__ = 'Geonu Choi'
__email__ = '6566gun@gmail.com'


class Handler(object):
    """Converting handler base.

    """
    def __init__(self, fn, domain=()):
        super(Handler, self).__init__()
        self.fn = fn
        self.domain = domain
        self.handlable = self.default_handlable

    def matching_type(self, obj):
        """Returns matching type in `domain` if exists, or :const:`None`

        :rtype: type

        """
        for t in self.domain:
            if isinstance(obj, t):
                return t
        return None

    def default_handlable(self, obj):
        """Default handlability checker. Just check type of instance.

        :rtype: bool

        """
        if self.matching_type(obj) is None:
            return False
        return True

    def __call__(self, obj):
        return self.fn(obj)

    def check_handlable(self, fn):
        """Decorator for function that indicates the handler can handle object.

        """
        self.handlable = fn
        return fn

    def can_handle(self, obj):
        return self.handlable(obj)


def _default_handler(self, obj):
    """Default convert handler.

    It just raises :class:`TypeError`

    """
    raise TypeError('Cannot convert object of {0}'.format(type(obj)))


class Converter(object):
    """Converts object into specified types."""

    def __init__(self, range):
        super(Converter, self).__init__()
        if isinstance(range, type):
            range = [range]
        self.range = range
        self.handlers = []
        self.default_handler = _default_handler

    def assert_type(self, obj):
        """Asserts if type of `obj` is in range of the converter."""
        for t in self.range:
            if isinstance(obj, t):
                return
        assert False, "{0!r} is not in range".format(obj)

    def inrange(self, obj):
        """Checks if `obj` is in range of the conveter.

        :rtype: bool

        """
        try:
            self.assert_type(obj)
        except AssertionError:
            return False
        return True

    def add_handler(self, handler):
        self.handlers.append(handler)

    def handle(self, *types):
        """Decorator for function that converts type.

        """
        def decorator(fn):
            handler = Handler(fn, types)
            wraps(fn)(handler)
            self.add_handler(handler)
            return handler
        return decorator

    def default(self, fn):
        """Decorator that changes default handler."""
        self.default_handler = fn
        return fn

    def find_handler(self, obj):
        """Finds best matching handler.
        Returns handler whose matching type is most-bottom subclass of class
        hierarchy tree.

        """
        candidates = [handler for handler in
                      self.handlers if
                      handler.can_handle(obj)]

        if not candidates:
            return None
        best = candidates.pop(0)
        while candidates:
            handler = candidates.pop(0)
            best_type = best.matching_type(obj)
            t = handler.matching_type(obj)
            if issubclass(t, best_type):
                best = handler
        return best

    def convert(self, obj):
        """Convert `obj` until it is in `range`."""
        while not self.inrange(obj):
            handler = self.find_handler(obj)
            if handler is None:
                handler = self.default_handler
            obj = handler(obj)
        return obj
