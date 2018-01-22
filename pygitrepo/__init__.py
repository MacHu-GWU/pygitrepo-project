#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .version import __version__

__short_description__ = (
    "Allow dummies develop Python project like a Pro - "
    "Quickly initiate a python project from scratch."
)
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .cli import initiate_project as init
except ImportError:  # pragma: no cover
    pass
