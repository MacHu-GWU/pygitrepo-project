# -*- coding: utf-8 -*-

"""
This module detects the current operation system.
"""

from __future__ import unicode_literals
import platform


class OSEnum(object):
    windows = "Windows"
    macOS = "Darwin"
    linux = "Linux"
    java = "Java"
    unknown = ""


OS_NAME = platform.system()  # type: str
IS_WINDOWS = OS_NAME == OSEnum.windows  # type: bool
IS_MACOS = OS_NAME == OSEnum.macOS  # type: bool
IS_LINUX = OS_NAME == OSEnum.linux  # type: bool
IS_JAVA = OS_NAME == OSEnum.java  # type: bool

if OS_NAME not in (OSEnum.windows, OSEnum.macOS, OSEnum.linux):
    raise EnvironmentError("Not supported OS: {}".format(OS_NAME))

if OS_NAME == OSEnum.windows:
    OPEN_COMMAND = "start"
elif OS_NAME in (OSEnum.macOS, OSEnum.linux):
    OPEN_COMMAND = "open"
else:
    OPEN_COMMAND = "unknown"
