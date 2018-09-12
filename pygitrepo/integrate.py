#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Integrate pyenv, tox, travis-ci.

pyenv is a great software to management multiple Python version and switch
between them.

It assumes you are developing your library on one version, and test over few
other version.

This module helps to convert pyenv specified version into tox, travis-ci
compatible version.
"""

import re
from collections import OrderedDict

import bs4
import requests

python_build_url = "https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build"


def _get_pyenv_versions_from_github():
    """
    Get all available pyenv version.
    """
    html = requests.get(python_build_url).text
    try:
        soup = bs4.BeautifulSoup(html, "html.parser")
    except:  # pragma: no cover
        soup = bs4.BeautifulSoup(html)

    versions = list()
    for div in soup.find_all("div", class_="file-wrap"):
        for table in div.find_all("table"):
            for td in table.find_all("td", class_="content"):
                for a in td.find_all("a"):
                    try:
                        title = a["title"]
                        if title != "patches":
                            if title == a.text:
                                versions.append(title)
                    except:  # pragma: no cover
                        pass

    return versions


def get_pyenv_versions():
    try:
        return _get_pyenv_versions_from_github()
    except:  # pragma: no cover
        return list()


pyenv_versions = get_pyenv_versions()


def validate_pyenv_ver(pyenv_ver):
    if pyenv_versions:
        if pyenv_ver not in pyenv_versions:
            raise ValueError(
                "%s is not a valid pyenv supported python version! "
                "Go to %s see supported version list." % (
                    pyenv_ver, python_build_url)
            )


def pyenv_ver_to_tox_ver(pyenv_ver):
    """
    Convert pyenv supported version to tox supported version.

    - `pyenv supported version <https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build>`_.
    - `tox supoorted version <http://tox.readthedocs.io/en/latest/example/basic.html#a-simple-tox-ini-default-environments>`_.

    Example:

        2.7.13 -> py27
        pypy3-2.4.0 -> pypy3
    """
    validate_pyenv_ver(pyenv_ver)

    special_version_mapper = OrderedDict([
        ("jython", "jython"),
        ("pypy3", "pypy3"),
        ("pypy", "pypy"),
        ("anaconda3", "py3"),
        ("anaconda2", "py2"),
        ("anaconda", "py"),
    ])

    for ver in special_version_mapper:
        if ver in pyenv_ver:
            return special_version_mapper[ver]

    # regular python version like 2/3.x.x
    py_ver_regex = "\d+.\d+"
    try:
        py_ver = re.findall(py_ver_regex, pyenv_ver)[0]

        if float(py_ver) < 2.6:  # 2.5 or earlier
            return "py2"
        if py_ver.startswith("2.6"):
            return "py26"
        if py_ver.startswith("2.7"):
            return "py27"

        if float(py_ver) < 3.3:  # 3.2 or earlier
            return "py3"
        if py_ver.startswith("3.3"):
            return "py33"
        if py_ver.startswith("3.4"):
            return "py34"
        if py_ver.startswith("3.5"):
            return "py35"
        if py_ver.startswith("3.6"):
            return "py36"
        if py_ver.startswith("3.7"):  # pragma: no cover
            return "py37"

        # for future version
        return "py" + pyenv_ver.replace(".", "")  # pragma: no cover
    except:  # pragma: no cover
        raise ValueError(
            "Cannot find supported tox version for %s!" % pyenv_ver)


def pyenv_ver_to_travis_ver(pyenv_ver):
    """
    Convert pyenv supported version to travis supported version.

    - `pyenv supported version <https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build>`_.
    - `travis.ci supoorted version <https://docs.travis-ci.com/user/languages/python/>`_.

    Example:

        2.7.13 -> 2.7
        pypy3-2.4.0 -> pypy3
    """
    validate_pyenv_ver(pyenv_ver)

    # solve pypy, anaconda
    special_version_mapper = OrderedDict([
        ("pypy3", "pypy3"),
        ("pypy", "pypy"),
        ("anaconda3", "3.4"),
        ("anaconda2", "2.7"),
        ("anaconda", "2.7"),
    ])

    for ver in special_version_mapper:
        if ver in pyenv_ver:
            return special_version_mapper[ver]

    # not supported version
    not_supported_version = [
        "ironpython", "jython", "miniconda", "pyston", "stackless",
    ]
    for ver in not_supported_version:
        if ver in pyenv_ver:
            raise ValueError("%s are not supported by travis!" % pyenv_ver)

    # dev version
    if pyenv_ver.endswith("-dev"):
        return pyenv_ver

    # regular python version like 2/3.x.x
    py_ver_regex = "\d+.\d+"

    try:
        py_ver = re.findall(py_ver_regex, pyenv_ver)[0]

        if float(py_ver) < 2.6:  # 2.5 or earlier
            raise ValueError("%s is not supported by travis!" % py_ver)

        if py_ver.startswith("2.6"):
            return "2.6"
        if py_ver.startswith("2.7"):
            return "2.7"

        if float(py_ver) < 3.2:  # 3.1 or earlier
            raise ValueError("%s is not supported by travis!" % py_ver)

        if py_ver.startswith("3.3"):
            return "3.3"
        if py_ver.startswith("3.4"):
            return "3.4"
        if py_ver.startswith("3.5"):
            return "3.5"
        if py_ver.startswith("3.6"):
            return "3.6"
        if py_ver.startswith("3.7"):  # pragma: no cover
            return "3.7"

        return py_ver
    except:
        raise ValueError(
            "Cannot find supported tox version for %s!" % pyenv_ver)
