#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from pygitrepo.validation import DocService
from pygitrepo.initiate_project import jinja2_render, initiate_project


def teardown_module(module):
    import shutil
    try:
        shutil.rmtree("brucelee-project")
    except:
        pass


def test_jinja2_render():
    template_content = "Title: {{ title }}"
    kwargs = dict(title="Hello World!")
    assert jinja2_render(template_content, kwargs) == "Title: Hello World!"


def test_initiate_project():
    package_name = "brucelee"  # IMPORTANT
    github_username = "Bruce-Lee"  # IMPORTANT
    supported_py_ver = ["2.7.13", "3.4.6", "3.5.3", "3.6.2"]  # IMPORTANT
    author_name = "Bruce Lee"  # IMPORTANT
    author_email = "brucelee@example.com"  # IMPORTANT
    rtd_name = None
    doc_host_bucket_name = None

    for doc_service in [DocService.readthedoc, DocService.s3, None]:
        initiate_project(
            package_name=package_name,
            github_username=github_username,
            supported_py_ver=supported_py_ver,
            author_name=author_name,
            author_email=author_email,
            license="OPEN SOURCE",
            rtd_name=rtd_name,
            doc_host_bucket_name=doc_host_bucket_name,
            doc_service=doc_service,
            verbose=True,
        )


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
