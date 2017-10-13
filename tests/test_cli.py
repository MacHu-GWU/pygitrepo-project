#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pygitrepo.cli import _initiate_project


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    import shutil
    try:
        shutil.rmtree("brucelee-project")
    except:
        pass


def test():
    package_name = "brucelee"  # IMPORTANT
    github_username = "Bruce-Lee"  # IMPORTANT
    supported_py_ver = ["2.7.13", "3.4.6", "3.5.3", "3.6.2"]  # IMPORTANT
    author_name = "Bruce Lee"  # IMPORTANT
    author_email = "brucelee@example.com"  # IMPORTANT
    s3_bucket = "www.bruce-lee.com"  # IMPORTANT

    _initiate_project(
        package_name=package_name,
        github_username=github_username,
        supported_py_ver=supported_py_ver,
        author_name=author_name,
        author_email=author_email,
        license="OPEN SOURCE",
        s3_bucket=s3_bucket,
    )


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
