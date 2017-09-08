#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script call pygitrepo-init from python.
"""

from pygitrepo.cli import _initiate_project

package_name = "test_blog"
github_username = "MacHu-GWU"
supported_py_ver = ["py27", "py34", "py35", "py36"]
author_name = "Sanhe Hu"
author_email = "husanhe@gmail.com"
s3_bucket = "www.wbh-doc.com"

if __name__ == "__main__":
    _initiate_project(
        package_name=package_name,
        github_username=github_username,
        supported_py_ver=supported_py_ver,
        author_name=author_name,
        author_email=author_email,
        license="MIT",
        s3_bucket=s3_bucket,
    )
