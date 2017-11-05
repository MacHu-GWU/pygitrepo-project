#!/usr/bin/env python
# -*- coding: utf-8 -*-


__version__ = "0.0.10"
__short_description__ = "Quickly initiate a python project from scratch."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"


try:
    from .cli import _initiate_project as init
except ImportError:  # pragma: no cover
    pass
