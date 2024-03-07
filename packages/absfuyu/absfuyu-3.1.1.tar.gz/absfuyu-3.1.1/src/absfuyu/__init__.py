"""
ABSFUYU
-------
A small collection of code

LINKS
-----
- [Home page](https://pypi.org/project/absfuyu/)
- [Documentation](https://absolutewinter.github.io/absfuyu/)

USAGE
-----

Normal import: 
>>> import absfuyu
>>> help(absfuyu)

Using in cmd (`absfuyu[cli]` required): 
``$ fuyu --help``
"""


# Module level
###########################################################################
__title__ = "absfuyu"
__author__ = "AbsoluteWinter"
__license__ = "MIT License"
__all__ = [
    "core",
    "config",
    "everything",
    "extensions",
    "logger",
    "fun",
    "game",
    "general",
    "pkg_data",
    "sort",
    "tools",
    "util",
    "version",
]


# Library
###########################################################################
from .version import __version__
