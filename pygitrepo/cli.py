#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script can generate automate scripts for open source python project.
"""

from __future__ import print_function
import click

from . import validation
from .initiate_project import initiate_project


def _validate_package_name(ctx, param, value):
    try:
        validation.validate_package_name(value)
        return value
    except Exception as e:
        click.secho(str(e), fg="red")
        value = click.prompt(param.prompt)
        return _validate_package_name(ctx, param, value)


def _validate_github_username(ctx, param, value):
    try:
        validation.validate_github_username(value)
        return value
    except Exception as e:
        click.secho(str(e), fg="red")
        value = click.prompt(param.prompt)
        return _validate_github_username(ctx, param, value)


def _validate_doc_service(ctx, param, value):
    try:
        value = validation.validate_doc_service(value)
        return value
    except Exception as e:
        click.secho(str(e), fg="red")
        value = click.prompt(param.prompt)
        return _validate_doc_service(ctx, param, value)


@click.command()
@click.option(
    "--package_name",
    prompt="(REQUIRED) Your Package Name (e.g. pip)",
    callback=_validate_package_name,
)
@click.option(
    "--repo_name",
    prompt="(optional) Your Repository Name (e.g. pip-project)",
    default="",
)
@click.option(
    "--github_username",
    prompt="(REQUIRED) Your Github Username",
    callback=_validate_github_username,
)
@click.option(
    "--supported_py_ver",
    prompt=(
            "(optional) Enter python version list your package will be tested with tox, "
            "seperate by comma. "
            "For example: '2.7.13, 3.4.6'. "
            "All available version are listed here: "
            "https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build"
    ),
    default="",
)
@click.option(
    "--author_name",
    prompt="(optional) Author Name",
    default="unknown author",
)
@click.option(
    "--author_email",
    prompt="(optional) Author Email",
    default="author@example.com",
)
@click.option(
    "--maintainer_name",
    prompt="(optional) Maintainer Name",
    default="unknown maintainer",
)
@click.option(
    "--maintainer_email",
    prompt="(optional) Maintainer Email",
    default="maintainer@example.com",
)
@click.option(
    "--rtd_name",
    prompt=(
            "(optional) If use ReadTheDocs to host your document, "
            "please specify the project name "
            "(will be your domain prefix)."
    ),
    default="",
)
@click.option(
    "--doc_host_bucket_name",
    prompt=(
            "(optional) If use AWS S3 to host your document, "
            "please specify the bucket name."
    ),
    default="",
)
@click.option(
    "--doc_service",
    prompt="(optional) Choose your doc host serivce from %s." % (
            " | ".join(validation.all_doc_service),),
    callback=_validate_doc_service,
    default="",
)
def _initiate_project(package_name,
                      repo_name,
                      github_username,
                      supported_py_ver,
                      author_name,
                      author_email,
                      maintainer_name,
                      maintainer_email,
                      rtd_name,
                      doc_host_bucket_name,
                      doc_service):
    if supported_py_ver is None:
        pass
    elif supported_py_ver.strip():
        supported_py_ver = [
            ver.strip().lower() for ver in supported_py_ver.split(",") if
            ver.strip()
        ]
    else:
        supported_py_ver = None

    initiate_project(
        package_name=package_name,
        repo_name=repo_name,
        github_username=github_username,
        supported_py_ver=supported_py_ver,
        author_name=author_name,
        author_email=author_email,
        maintainer_name=maintainer_name,
        maintainer_email=maintainer_email,
        rtd_name=rtd_name,
        doc_host_bucket_name=doc_host_bucket_name,
        doc_service=doc_service,
    )
