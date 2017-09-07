#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script instantly 'install' (actually copy it to ``site-packages`` dir)
your package, make it available to import for the current python interpreter,
even it's a virtualenv.

require: pypi.python.org/pypi/ezinstall
"""

if __name__ == "__main__":
    import os
    from ezinstall import install

    install(os.path.dirname(__file__))
