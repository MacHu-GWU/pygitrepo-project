# -*- coding: utf-8 -*-

"""
This module detects the current operation system.
"""

from __future__ import unicode_literals
import platform


class OSEnum(object):
    """
    Operation System name enumeration.
    """
    windows = "Windows"
    macOS = "Darwin"
    linux = "Linux"
    java = "Java"
    unknown = ""


OS_NAME = platform.system()  # type: str
"""
Current OS name
"""

IS_WINDOWS = OS_NAME == OSEnum.windows  # type: bool
"""
Boolean value that indicate if the current OS is Windows 
"""

IS_MACOS = OS_NAME == OSEnum.macOS  # type: bool
"""
Boolean value that indicate if the current OS is MacOS 
"""

IS_LINUX = OS_NAME == OSEnum.linux  # type: bool
"""
Boolean value that indicate if the current OS is Linux 
"""

IS_JAVA = OS_NAME == OSEnum.java  # type: bool
"""
Boolean value that indicate if the current OS is Java 
"""

if OS_NAME not in (OSEnum.windows, OSEnum.macOS, OSEnum.linux):
    raise EnvironmentError("Not supported OS: {}".format(OS_NAME))

OPEN_COMMAND = None
"""
The OS dependent command that open a file in default application.
"""
if OS_NAME == OSEnum.windows:
    OPEN_COMMAND = "start"
elif OS_NAME in (OSEnum.macOS, OSEnum.linux):
    OPEN_COMMAND = "open"
else:
    OPEN_COMMAND = "unknown"
