# -*- coding: utf-8 -*-

"""
Utility module for colored text print in terminal.
"""

import os

from .pkg.mini_colorma import Fore, Style

TAB = " " * 2


def pgr_print(message):
    """
    Syntax sugar for:

    [pygitrepo] ... message ... {Style.RESET_ALL}

    :type message: str
    """
    print("[pygitrepo] {}{}".format(message, Style.RESET_ALL))


def pgr_print_done(indent=0):
    """
    Syntax sugar for:

    [pygitrepo] {number_of_tab_indent}done

    :type indent: int
    """
    print("{reset}[pygitrepo] {cyan}{indent}done{reset}".format(
        cyan=Fore.CYAN,
        reset=Style.RESET_ALL,
        indent=indent * TAB,
    ))


def colorful_path(path):
    """
    :type path: str
    :rtype: str
    """
    if os.path.exists(path):
        color = Fore.GREEN
    else:
        color = Fore.RED
    return "{color}{path}{reset}".format(
        color=color,
        path=path,
        reset=Style.RESET_ALL,
    )


def print_path(title, path):
    """
    Print a description of a path and the absolute path. If path exists,
    path is in green, if not exists, path is in red.

    Example: "- virtual environment directory: /path-to/my_venv"

    :type title: str
    :type path: str
    """
    if os.path.exists(path):
        color = Fore.GREEN
    else:
        color = Fore.RED
    msg = "{reset}- {cyan}{title}: {colorful_path}".format(
        reset=Style.RESET_ALL,
        cyan=Fore.CYAN,
        color=color,
        title=title,
        colorful_path=colorful_path(path),
    )
    print(msg)


def print_line(msg):
    """
    Color print a message reset style before and after.

    :type msg: str
    :rtype: str
    """
    print("{reset}{msg}{reset}".format(reset=Style.RESET_ALL, msg=msg))
