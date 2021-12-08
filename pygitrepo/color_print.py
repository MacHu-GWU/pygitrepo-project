# -*- coding: utf-8 -*-

import os
from .pkg.mini_colorma import Fore, Back, Style

TAB = " " * 2


def pgr_print(message):
    """
    "[pygitrepo] ... message ... {Style.RESET_ALL}
    """
    print("[pygitrepo] {}{}".format(message, Style.RESET_ALL))


def pgr_print_done(indent=0):
    print("[pygitrepo] {}{}done{}".format(
        Fore.CYAN,
        indent * TAB,
        Style.RESET_ALL,
    ))


def print_path(title, path):
    """
    Print ``- virtual environment directory: /path-to/my_venv``
    """
    if os.path.exists(path):
        color = Fore.GREEN
    else:
        color = Fore.RED
    msg = "{reset}- {cyan}{title}: {color}{path}{reset}".format(
        reset=Style.RESET_ALL,
        cyan=Fore.CYAN,
        color=color,
        title=title,
        path=path,
    )
    print(msg)


def print_line(msg):
    """
    Color print a message reset style before and after.

    :type msg: str
    :rtype: str
    """
    print("{reset}{msg}{reset}".format(reset=Style.RESET_ALL, msg=msg))


def colorful_path(path):
    """
    :type path: str
    :rtype: str
    """
    if os.path.exists(path):
        color = Fore.GREEN
    else:
        color = Fore.Red
    return "{color}{path}{reset}".format(
        color=color,
        path=path,
        reset=Style.RESET_ALL,
    )
