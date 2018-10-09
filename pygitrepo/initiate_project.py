#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script can generate automate scripts for open source python project.
"""

from __future__ import print_function
import sys
import datetime
from os import walk, mkdir, getcwd

import click
from jinja2 import Template
from pathlib_mate import Path

from . import integrate, validation
from .util import read, write
from .version import __version__

py_ver_major = sys.version_info.major
py_ver_minor = sys.version_info.minor
py_ver_micro = sys.version_info.micro

py_ver_long = "%s.%s.%s" % (py_ver_major, py_ver_minor, py_ver_micro)
py_ver_short = "%s.%s" % (py_ver_major, py_ver_minor)


UNKNOWN_S3_BUCKET_NAME = "Unknwon-S3-Bucket-Name"


def jinja2_render(template_content, kwargs):
    template = Template(template_content)
    return template.render(**kwargs)


def initiate_project(package_name=None,
                     repo_name=None,
                     github_username=None,
                     supported_py_ver=None,
                     author_name="unknown author",
                     author_email="unknown@example.com",
                     maintainer_name=None,
                     maintainer_email=None,
                     license="MIT",
                     rtd_name=None,
                     doc_host_bucket_name=None,
                     doc_service=None,
                     verbose=True,
                     **kwargs):
    """
    Generate skeleton of project files.

    :param package_name: your python package name, it should be able to install
        via ``pip install <package_name>``, and will be published on
        https://pypi.python.org/pypi/package_name

    :param repo_name: github repository name, the github link will be:
        https://github.com/github_username/repo_name

    :param github_username: github username, the github link will be:
        https://github.com/github_username/repo_name

    :param supported_py_ver: list of Python version you want to support,
        it has to be a valid pyenv version.
        available Python Version names can be found at:
        https://github.com/pyenv/pyenv/blob/master/plugins/python-build/share/python-build.

    :param author_name: author name
    :param author_email: author email
    :param maintainer_name: maintainer name
    :param maintainer_email: maintainer email

    :param license: currently only support MIT license, you can manually replace
        the license file yourself.

    :param rtd_name: Read the doc project name, doc will be host at:
        https://rtd_name.readthedocs.io/

    :param doc_host_bucket_name: AWS S3 bucket name, doc will be host at
        http://doc_host_bucket_name.s3.amazonaws.com/package_name/index.html. You need to
        config your bucket to allow all public get traffic. Tutorial is here:
        http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html

    :param doc_service: str, doc service you want to use, one of "rtd", "s3".

    :param verbose: bool, toggle on / off the log info.
    """
    validation.validate_package_name(package_name)

    if not bool(repo_name):  # pragma: no cover
        repo_name = "{}-project".format(package_name)

    validation.validate_github_username(github_username)
    repo_url = "https://github.com/{github_username}/{repo_name}" \
        .format(github_username=github_username, repo_name=repo_name)

    # if not provided, use the current interpreter.
    if not bool(supported_py_ver):  # pragma: no cover
        supported_py_ver = [py_ver_long, ]

    supported_py_ver_for_tox = set()
    for py_ver in supported_py_ver:
        try:
            supported_py_ver_for_tox.add(
                integrate.pyenv_ver_to_tox_ver(py_ver)
            )
        except Exception as e:  # pragma: no cover
            click.echo(str(e))
    supported_py_ver_for_tox = list(supported_py_ver_for_tox)
    supported_py_ver_for_tox.sort()

    supported_py_ver_for_tarvis = set()
    for py_ver in supported_py_ver:
        try:
            supported_py_ver_for_tarvis.add(
                integrate.pyenv_ver_to_travis_ver(py_ver)
            )
        except Exception as e:  # pragma: no cover
            print(e)
    supported_py_ver_for_tarvis = list(supported_py_ver_for_tarvis)
    supported_py_ver_for_tarvis.sort()

    if license != "MIT":  # pragma: no cover
        license = "MIT"
    click.secho(
        ("Initiate with a MIT license, "
         "you can manually change the file yourself!"),
        fg="red",
    )

    if not bool(rtd_name):  # pragma: no cover
        rtd_name = "Unknown_ReadTheDocs_Project_Name"
    doc_domain_rtd = "https://{rtd_name}.readthedocs.io".format(
        rtd_name=rtd_name)

    if not bool(doc_host_bucket_name):  # pragma: no cover
        doc_host_bucket_name = UNKNOWN_S3_BUCKET_NAME
    doc_domain_s3 = "http://{s3_bucket}.s3.amazonaws.com/{package_name}" \
        .format(s3_bucket=doc_host_bucket_name, package_name=package_name)

    validation.validate_doc_service(doc_service)
    doc_domain = None
    if doc_service is None:  # pragma: no cover
        click.secho(
            ("You don't have a website to host your documents! "
             "You could use either https://readthedocs.org or AWS S3."),
            fg="green"
        )
    elif doc_service == validation.DocService.readthedoc:  # pragma: no cover
        doc_domain = doc_domain_rtd
    elif doc_service == validation.DocService.s3:  # pragma: no cover
        doc_domain = doc_domain_s3
    else:  # pragma: no cover
        raise ValueError(
            "doesn't recognize doc host service '%s'!" % doc_service)

    click.secho(
        (
            "There's author introduction file at '{repo_name}/docs/source/author.rst', "
            "you should change it to your own self introduction.")
            .format(repo_name=repo_name),
        fg="red",
    )
    click.secho(
        (
            "There are logo files at '{repo_name}/docs/source/_static', "
            "you should replace it with your own project logo.")
            .format(repo_name=repo_name),
        fg="red",
    )

    if not maintainer_name:  # pragma: no cover
        maintainer_name = author_name

    if not maintainer_email:  # pragma: no cover
        maintainer_email = author_email

    kwargs_ = dict(
        pygitrepo_version=__version__,
        package_name=package_name,
        repo_name=repo_name,
        github_username=github_username,
        repo_url=repo_url,

        supported_py_ver=supported_py_ver,
        supported_py_ver_for_tox=supported_py_ver_for_tox,
        supported_py_ver_for_travis=supported_py_ver_for_tarvis,

        py_ver_major=py_ver_major,
        py_ver_minor=py_ver_minor,
        py_ver_micro=py_ver_micro,

        year=datetime.datetime.utcnow().year,
        today=datetime.date.today(),

        license=license,

        author_name=author_name,
        author_email=author_email,
        maintainer_name=maintainer_name,
        maintainer_email=maintainer_email,

        doc_service=doc_service,
        rtd_name=rtd_name,
        doc_host_bucket_name=doc_host_bucket_name,
        doc_domain=doc_domain,
    )
    kwargs_.update(kwargs)

    # Create files
    print("Initate '%s' from template ..." % repo_name)

    template_dir = Path(__file__).absolute().change(
        new_basename="{{ repo_name }}")
    output_dir = Path(getcwd(), repo_name).absolute()

    file_count = 0
    for src_dir, dir_list, file_list in walk(template_dir.abspath):
        file_list = list(file_list)
        file_list.sort()

        if src_dir.endswith("__pycache__"):  # pragma: no cover
            continue

        # find destination directory
        dst_dir = Path(
            jinja2_render(
                src_dir.replace(template_dir.abspath, output_dir.abspath, 1),
                kwargs_,
            )
        )

        # make destination directory
        try:
            if verbose:
                print("    Create '%s' ..." % dst_dir)
            mkdir(dst_dir.abspath)
        except:  # pragma: no cover
            pass

        # files
        for filename in file_list:
            if filename.endswith(".pyc") or filename.endswith(
                    ".DS_Store"):  # pragma: no cover
                continue

            src = Path(src_dir, filename)
            dst = Path(
                jinja2_render(
                    Path(dst_dir.abspath, filename).abspath,
                    kwargs_,
                )
            )

            try:  # text file
                content = jinja2_render(read(src.abspath), kwargs_)
                if verbose:
                    print("    Create '%s' ..." % dst)
                write(content, dst.abspath)
            except:  # binary file
                src.copyto(new_abspath=dst.abspath, overwrite=True)

            file_count += 1

    print("    COMPLETE! %s files created." % file_count)
