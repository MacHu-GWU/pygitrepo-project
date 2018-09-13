#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
import string


def validate_not_none(param, value):
    if value is None:
        msg = "`{}` can't be None!".format(param)
        raise ValueError(msg)


def validate_not_empty_string(param, value):
    if isinstance(value, six.string_types):
        if len(value) == 0:
            msg = "`{}` can't be empty string!".format(param)
            raise ValueError(msg)
    else:
        msg = "`{}` has to be a string!".format(param)
        raise TypeError(msg)


_package_name_charset = string.ascii_letters + string.digits + "_"
package_name_charset = set(_package_name_charset)
_github_username_charset = string.ascii_letters + string.digits + "-"
github_username_charset = set(_github_username_charset)


def validate_package_name(package_name):
    validate_not_none(param="package_name", value=package_name)
    validate_not_empty_string(param="package_name", value=package_name)
    invalid_charset = set(package_name).difference(package_name_charset)
    if len(invalid_charset):
        msg = "`package_name` can only contains '{}'!".format(
            _package_name_charset)
        raise ValueError(msg)
    if package_name[0] in string.digits:
        msg = "`package_name` can't start with digits!"
        raise ValueError(msg)


def validate_github_username(github_username):
    validate_not_none(param="github_username", value=github_username)
    validate_not_empty_string(param="github_username", value=github_username)
    invalid_charset = set(github_username).difference(github_username_charset)
    if len(invalid_charset):
        msg = "`github_username` can only contains '{}'!".format(
            _github_username_charset)
        raise ValueError(msg)
    if github_username[0] == "-":
        msg = "`github_username` can't start with hyphen!"
        raise ValueError(msg)
    if github_username[-1] == "-":
        msg = "`github_username` can't end with hyphen!"
        raise ValueError(msg)


class DocService(object):
    readthedoc = "rtd"
    s3 = "s3"


all_doc_service = [
    DocService.readthedoc,
    DocService.s3,
]

doc_service_nullable_values = ["none", "null", ""]


def validate_doc_service(doc_service):
    if doc_service is None:
        return None

    if doc_service.strip().lower() in doc_service_nullable_values:
        return None

    if doc_service not in all_doc_service:
        msg = "`doc_service` has to be one of {}".format(", ".join(all_doc_service))
        raise ValueError(msg)
