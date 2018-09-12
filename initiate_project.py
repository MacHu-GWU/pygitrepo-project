#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script call pygitrepo-init from python.
"""

import pygitrepo

package_name = "pygitrepo"
repo_name = None
github_username = "MacHu-GWU"
supported_py_ver = ["2.7.13", "3.4.6", "3.5.3", "3.6.2"]
author_name = "Sanhe Hu"
author_email = "husanhe@gmail.com"
license = "MIT"
rtd_name = package_name
doc_host_bucket_name = "your-s3-bucket-name"
doc_service = "rtd"  # "none", "rtd", "s3"


if __name__ == "__main__":
    pygitrepo.init(
        package_name=package_name,
        repo_name=repo_name,
        github_username=github_username,
        supported_py_ver=supported_py_ver,
        author_name=author_name,
        author_email=author_email,
        license=license,
        rtd_name=rtd_name,
        doc_host_bucket_name=doc_host_bucket_name,
        doc_service=doc_service,
    )
