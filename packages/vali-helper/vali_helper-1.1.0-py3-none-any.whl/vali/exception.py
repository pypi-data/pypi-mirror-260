# -*- encoding: utf8 -*-
"""
This module defines all the exceptions that are used in this package
"""

__all__ = [
    'ValiFailError',
    'UnsupportedError',
    'PackageNotExistError',
]


class ValiFailError(Exception):
    """
    The exception would be raised when validation failed.
    """
    def __init__(self, message):
        self.message = message


class UnsupportedError(Exception):
    """
    The exception would be raised in unsupported operation
    """

    def __init__(self, msg):
        self.message = msg


class PackageNotExistError(Exception):
    """
    The exception that there is no package "python-dateutil" installed
    """

    def __init__(self):
        self.message = 'Cannot import package "python-dateutil", '\
                       'please ensure it is installed in current environment.'\
                       'It could be installed by "pip install vali[dateutil]"'\
                       'Or use "datetime" or "date" to instead of "str"'
