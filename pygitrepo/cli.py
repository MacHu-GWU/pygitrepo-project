#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script can generate automate scripts for open source python project.

Scroll to ``if __name__ == "__main__":`` for more info.
"""

from __future__ import print_function
import sys
import datetime
from os import walk, mkdir, getcwd

import click
from jinja2 import Template
from pathlib_mate.pathlib import Path

try:
    from .util import read, write
except:  # pragma: no cover
    from pygitrepo.util import read, write

py_ver_major = sys.version_info.major
py_ver_minor = sys.version_info.minor
py_ver_micro = sys.version_info.micro

py_ver_long = "%s.%s.%s" % (py_ver_major, py_ver_minor, py_ver_micro)
py_ver_short = "%s.%s" % (py_ver_major, py_ver_minor)


def simple_render(template_content, kwargs):  # pragma: no cover
    """Redner a jinja2 styled template.

    :param template_content: str
    :param kwargs: dict
    :return:
    """
    temp_prefix = "{{ PyGitRepo_Temp_Prefix____%s }}"
    mapper1, mapper2 = dict(), dict()
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


def _initiate_project(package_name=None,
                      repo_name=None,
                      github_username=None,
                      supported_py_ver=None,
                      author_name=None,
                      author_email=None,
                      maintainer_name=None,
                      maintainer_email=None,
                      license="MIT",
                      s3_bucket=None,
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

    :param supported_py_ver: list of py environment you want to support,
      available test environment names can be found at
      http://tox.readthedocs.io/en/latest/example/basic.html#a-simple-tox-ini-default-environments

    :param supported_py_ver_for_travis: list of py environment you want to test
      with https://travis-ci.org/. available test environment can be found at:
      https://docs.travis-ci.com/user/languages/python/

    :param author_name: author name
    :param author_email: author email
    :param maintainer_name: maintainer name
    :param maintainer_email: maintainer email

    :param license: currently only support MIT license, you can manually replace
      the license file yourself.

    :param s3_bucket: AWS S3 bucket name, doc will be host at
      http://<s3_bucket>.s3.amazonaws.com/<package_name>/index.html
    """
    if not package_name:  # pragma: no cover
        raise ValueError("`package_name` can't be None!")

    if not repo_name:
        repo_name = "%s-project" % package_name

    if not github_username:  # pragma: no cover
        raise ValueError("`github_username` can't be None!")

    if not supported_py_ver:
        supported_py_ver = ["py27", "py34"]

    mapper = dict(
        py="2.7",
        py2="2.7",
        py3="3.4",
        py26="2.6",
        py27="2.7",
        py33="3.3",
        py34="3.4",
        py35="3.5",
        py36="3.6",
        py37="3.7",
        pypy="pypy",
        pypy3="pypy3",
    )
    supported_py_ver_for_travis = list(set([
        mapper.get(py_ver, py_ver) for py_ver in supported_py_ver
    ]))
    supported_py_ver_for_travis.sort()

    if license != "MIT":  # pragma: no cover
        license = "MIT"
        print("Initiate with MIT license, "
              "you can manually replace the file yourself!")

    if not s3_bucket:  # pragma: no cover
        s3_bucket = "Unknown-S3-Bucket-Name"

    if not maintainer_name:  # pragma: no cover
        maintainer_name = author_name

    if not maintainer_email:  # pragma: no cover
        maintainer_email = author_email

    kwargs_ = dict(
        package_name=package_name,
        repo_name=repo_name,
        github_username=github_username,

        supported_py_ver=supported_py_ver,
        supported_py_ver_for_travis=supported_py_ver_for_travis,

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
        s3_bucket=s3_bucket,
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
            print("    Create '%s' ..." % dst_dir)
            mkdir(dst_dir.abspath)
        except:  # pragma: no cover
            pass

        # files
        for filename in file_list:
            if filename.endswith(".pyc") or filename.endswith(".DS_Store"):  # pragma: no cover
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
                print("    Create '%s' ..." % dst)
                write(content, dst.abspath)
            except:  # binary file
                src.copyto(new_abspath=dst.abspath, overwrite=True)

            file_count += 1

    print("    COMPLETE! %s files created." % file_count)


@click.command()  # pragma: no cover
@click.option("--package_name",
              prompt="Your Package Name (e.g. pip)")
@click.option("--repo_name",
              prompt="(optional) Your Repository Name (e.g. pip-project)",
              default="")
@click.option("--github_username",
              prompt="Your Github Username")
@click.option("--supported_py_ver",
              prompt=("(optional) Enter python version list your package will support, "
                      "seperate by comma. All available version are listed here: "
                      "https://tox.readthedocs.io/en/latest/example/basic.html"),
              default="")
@click.option("--author_name",
              prompt="Author Name",
              default="")
@click.option("--author_email",
              prompt="Author Email",
              default="")
@click.option("--maintainer_name",
              prompt="Maintainer Name",
              default="")
@click.option("--maintainer_email",
              prompt="Maintainer Email",
              default="")
@click.option("--s3_bucket",
              prompt="S3 Bucket",
              default="")
def initiate_project(package_name,
                     repo_name,
                     github_username,
                     supported_py_ver,
                     author_name,
                     author_email,
                     maintainer_name,
                     maintainer_email,
                     s3_bucket,
                     **kwargs):
    if supported_py_ver is None:
        pass
    elif supported_py_ver.strip():
        supported_py_ver = [
            ver.strip().lower() for ver in supported_py_ver.split(",") if ver.strip()
        ]
    else:  # pragma: no cover
        supported_py_ver = None

    _initiate_project(package_name=package_name,
                      repo_name=repo_name,
                      github_username=github_username,
                      supported_py_ver=supported_py_ver,
                      author_name=author_name,
                      author_email=author_email,
                      maintainer_name=maintainer_name,
                      maintainer_email=maintainer_email,
                      s3_bucket=s3_bucket,
                      **kwargs)


if __name__ == "__main__":
    initiate_project()
