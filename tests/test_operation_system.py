# -*- coding: utf-8 -*-

import pytest


def test():
    from pygitrepo.operation_system import (
        OS_NAME, IS_WINDOWS, IS_MACOS, IS_LINUX, IS_JAVA,
        OPEN_COMMAND,
    )


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
