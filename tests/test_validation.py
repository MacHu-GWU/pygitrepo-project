#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from pygitrepo import validation


def test_validate_not_none():
    validation.validate_not_none("param", "Hello World!")
    validation.validate_not_none("param", "")
    with raises(ValueError):
        validation.validate_not_none("param", None)


def test_validate_not_empty_string():
    validation.validate_not_empty_string("param", "Hello World!")
    with raises(ValueError):
        validation.validate_not_empty_string("param", "")
    with raises(TypeError):
        validation.validate_not_empty_string("param", 1)


def test_validate_package_name():
    validation.validate_package_name("requests")
    validation.validate_package_name("requests_mate")

    with raises(ValueError):
        validation.validate_package_name("pip env")
    with raises(ValueError):
        validation.validate_package_name("1requests")


def test_validate_github_username():
    validation.validate_github_username("david")
    validation.validate_github_username("david-john")

    with raises(ValueError):
        validation.validate_github_username("david john")
    with raises(ValueError):
        validation.validate_github_username("-david-john")
    with raises(ValueError):
        validation.validate_github_username("david-john-")


def test_validate_doc_service():
    validation.validate_doc_service(None)
    validation.validate_doc_service("null")
    validation.validate_doc_service("none")
    validation.validate_doc_service("")
    validation.validate_doc_service(validation.DocService.readthedoc)
    validation.validate_doc_service(validation.DocService.s3)

    with raises(ValueError):
        validation.validate_doc_service("something else")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
