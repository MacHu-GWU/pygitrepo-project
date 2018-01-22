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
from pathlib_mate.pathlib import Path

try:
    from . import integrate
    from .util import read, write
    from .version import __version__
except:  # pragma: no cover
    from pygitrepo import integrate
    from pygitrepo.util import read, write
    from pygitrepo.version import __version__


py_ver_major = sys.version_info.major
py_ver_minor = sys.version_info.minor
py_ver_micro = sys.version_info.micro

py_ver_long = "%s.%s.%s" % (py_ver_major, py_ver_minor, py_ver_micro)
py_ver_short = "%s.%s" % (py_ver_major, py_ver_minor)


def simple_render(template_content, kwargs):  # pragma: no cover
    """
    Rend a jinja2 styled template.

    :param template_content: str
    :param kwargs: dict
    """
    temp_prefix = "{{ PyGitRepo_Temp_Prefix____%s }}"
    mapper1 = dict()
    """
    {"{{ name }}": "{{ PyGitRepo_Temp_Prefix____name }}"
    """
    mapper2 = dict()
    """
    {"{{ PyGitRepo_Temp_Prefix____name }}": value}
    """
    for i, (key, value) in enumerate(kwargs.items()):
        temp_key = temp_prefix % i
        mapper1["{{ %s }}" % key] = temp_key
        mapper2[temp_key] = str(value)
    for old, new in mapper1.items():
        template_content = template_content.replace(old, new)
    for old, new in mapper2.items():
        template_content = template_content.replace(old, new)
    return template_content


def jinja2_render(template_content, kwargs):  # pragma: no cover
    template = Template(template_content)
    return template.render(**kwargs)


def is_none_or_empty(value):
    """
    Test if a value is None or 'False' things.
    """
    if (value is None) or (bool(value) is False):
        return True
    else:
        return False

SUPPORT_DOC_HOST_SERVICE = ["none", "rtd", "s3"]

def initiate_project(package_name=None,
                     repo_name=None,
                     github_username=None,
                     supported_py_ver=None,
                     author_name=None,
                     author_email=None,
                     maintainer_name=None,
                     maintainer_email=None,
                     license="MIT",
                     rtd_name=None,
                     s3_bucket=None,
                     doc_service="none",
                     verbose=True,
                     **kwargs):
    """
    Generate skeleton of project files.

    :param package_name: your python package name, it should be able to install
        via ``pip install <package_name>``, and will be published on
        https://pypi.python.org/pypi/<package_name>

    :param repo_name: github repository name, the github link will be:
        https://github.com//<github_username>/<repo_name>

    :param github_username: github username, the github link will be:
        https://github.com//<github_username>/<repo_name>

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
        http://<rtd_name>.readthedocs.io/

    :param s3_bucket: AWS S3 bucket name, doc will be host at
        http://<s3_bucket>.s3.amazonaws.com/<package_name>/index.html. You need to
        config your bucket to allow all public get traffic. Tutorial is here:
        http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html

    :param doc_service: str, doc service you want to use, one of
        "none", "rtd", "s3".

    :param verbose: bool, toggle on / off the log info.
    """
    if is_none_or_empty(package_name):  # pragma: no cover
        raise ValueError("`package_name` can't be None!")

    if is_none_or_empty(repo_name):  # pragma: no cover
        repo_name = "%s-project" % package_name

    if is_none_or_empty(github_username):  # pragma: no cover
        raise ValueError("`github_username` can't be None!")
    else:
        repo_url = "https://github.com/{github_username}/{repo_name}" \
            .format(github_username=github_username, repo_name=repo_name)

    # if not provided, use the current intepreter.
    if is_none_or_empty(supported_py_ver):  # pragma: no cover
        supported_py_ver = [py_ver_long, ]

    supported_py_ver_for_tox = set()
    for py_ver in supported_py_ver:
        try:
            supported_py_ver_for_tox.add(
                integrate.pyenv_ver_to_tox_ver(py_ver)
            )
        except Exception as e:  # pragma: no cover
            print(e)
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

    if is_none_or_empty(rtd_name) is False:  # pragma: no cover
        doc_domain_rtd = "https://{rtd_name}.readthedocs.io" \
            .format(rtd_name=rtd_name)
    else: # pragma: no cover
        rtd_name = "Unknown_ReadTheDocs_Project_Name"

    if is_none_or_empty(s3_bucket) is False:  # pragma: no cover
        doc_domain_s3 = "http://{s3_bucket}.s3.amazonaws.com/{package_name}" \
            .format(s3_bucket=s3_bucket, package_name=package_name)
    else: # pragma: no cover
        s3_bucket = "Unknwon_S3_Bucket_Name"

    doc_domain = None
    if doc_service == "none": # pragma: no cover
        click.secho(
            ("You don't have a website to host your documents! "
             "You could use either https://readthedocs.org or AWS S3."),
            fg="green"
        )
    elif doc_service == "rtd": # pragma: no cover
        doc_domain = doc_domain_rtd
    elif doc_service == "s3": # pragma: no cover
        doc_domain = doc_domain_s3
    else: # pragma: no cover
        raise ValueError("doesn't recognize doc host service '%s'!" % doc_service)

    click.secho(
        (
        "There's author introduction file at {repo_name}/docs/source/author.rst, "
        "you should change it to your own introduction.") \
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

        rtd_name=rtd_name,
        s3_bucket=s3_bucket,
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


@click.command()  # pragma: no cover
@click.option(
    "--package_name",
    prompt="(REQUIRED) Your Package Name (e.g. pip)",
)
@click.option(
    "--repo_name",
    prompt="(optional) Your Repository Name (e.g. pip-project)",
    default="",
)
@click.option(
    "--github_username",
    prompt="(REQUIRED) Your Github Username",
)
@click.option(
    "--supported_py_ver",
    prompt=(
        "(optional) Enter python version list your package will support, "
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
    default="",
)
@click.option(
    "--author_email",
    prompt="(optional) Author Email",
    default="",
)
@click.option(
    "--maintainer_name",
    prompt="(optional) Maintainer Name",
    default="",
)
@click.option(
    "--maintainer_email",
    prompt="(optional) Maintainer Email",
    default="",
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
    "--s3_bucket",
    prompt=(
          "(optional) If use AWS S3 to host your document, "
          "please specify the bucket name."
    ),
    default="",
)
@click.option(
    "--doc_service",
    prompt="(REQUIRED) Choose your doc host serivce from %s." % (
        " | ".join(SUPPORT_DOC_HOST_SERVICE), ),
    type=click.Choice(SUPPORT_DOC_HOST_SERVICE),
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
                      s3_bucket,
                      doc_service):
    if supported_py_ver is None:
        pass
    elif supported_py_ver.strip():
        supported_py_ver = [
            ver.strip().lower() for ver in supported_py_ver.split(",") if
            ver.strip()
        ]
    else:  # pragma: no cover
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
        s3_bucket=s3_bucket,
        doc_service=doc_service,
    )


if __name__ == "__main__":
    initiate_project()
