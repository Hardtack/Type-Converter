# -*- encoding: utf-8 -*-
"""TypeConverter
~~~~~~~~~~~~~~~~~

Quick and dirty python type converter.

"""
from setuptools import setup

from typeconverter import (__version__ as version, __license__ as license,
                           __author__ as author, __email__ as email)

setup(
    name='TypeConverter',
    version=version,
    py_modules=['typeconverter'],
    url='https://github.com/hardtack/typeconverter',
    license=license,
    author=author,
    author_email=email,
    description='Simple type converter',
    long_description=__doc__,
)
