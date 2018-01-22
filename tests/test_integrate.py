#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from pygitrepo.integrate import (
    _get_pyenv_versions_from_github,
    pyenv_ver_to_tox_ver, pyenv_ver_to_travis_ver,
)


def test_get_pyenv_versions_from_github():
    versions = _get_pyenv_versions_from_github()
    assert "2.7.13" in versions
    assert "3.4.6" in versions


def test_pyenv_ver_to_tox_ver():
    assert pyenv_ver_to_tox_ver("2.5.6") == "py2"
    assert pyenv_ver_to_tox_ver("2.6.9") == "py26"
    assert pyenv_ver_to_tox_ver("2.7.13") == "py27"
    assert pyenv_ver_to_tox_ver("2.7-dev") == "py27"

    assert pyenv_ver_to_tox_ver("3.2.6") == "py3"
    assert pyenv_ver_to_tox_ver("3.3.6") == "py33"
    assert pyenv_ver_to_tox_ver("3.4.6") == "py34"
    assert pyenv_ver_to_tox_ver("3.5.3") == "py35"
    assert pyenv_ver_to_tox_ver("3.6.2") == "py36"
    assert pyenv_ver_to_tox_ver("3.6-dev") == "py36"
    assert pyenv_ver_to_tox_ver("3.7-dev") == "py37"

    assert pyenv_ver_to_tox_ver("anaconda-4.0.0") == "py"
    assert pyenv_ver_to_tox_ver("anaconda2-4.4.0") == "py2"
    assert pyenv_ver_to_tox_ver("anaconda3-4.4.0") == "py3"

    assert pyenv_ver_to_tox_ver("jython-dev") == "jython"
    assert pyenv_ver_to_tox_ver("jython-2.7.0") == "jython"

    with raises(Exception):
        pyenv_ver_to_tox_ver("Something")


def test_pyenv_ver_to_travis_ver():
    with raises(Exception):
        pyenv_ver_to_travis_ver("2.5.6")

    assert pyenv_ver_to_travis_ver("2.6.9") == "2.6"
    assert pyenv_ver_to_travis_ver("2.7.13") == "2.7"
    assert pyenv_ver_to_travis_ver("2.7-dev") == "2.7-dev"

    with raises(Exception):
        pyenv_ver_to_travis_ver("3.1.5")

    assert pyenv_ver_to_travis_ver("3.2.6") == "3.2"
    assert pyenv_ver_to_travis_ver("3.3.6") == "3.3"
    assert pyenv_ver_to_travis_ver("3.4.6") == "3.4"
    assert pyenv_ver_to_travis_ver("3.5.3") == "3.5"
    assert pyenv_ver_to_travis_ver("3.6.2") == "3.6"
    assert pyenv_ver_to_travis_ver("3.6-dev") == "3.6-dev"
    assert pyenv_ver_to_travis_ver("3.7-dev") == "3.7-dev"

    assert pyenv_ver_to_travis_ver("anaconda-4.0.0") == "2.7"
    assert pyenv_ver_to_travis_ver("anaconda2-4.4.0") == "2.7"
    assert pyenv_ver_to_travis_ver("anaconda3-4.4.0") == "3.4"

    vers = [
        "ironpython-dev", "ironpython-2.7.7",
        "jython-dev", "jython-2.7.0", "jython-2.7.1b3",
        "pyston-0.6.1",
        "stackless-dev", "stackless-3.4.2",
    ]
    for v in vers:
        with raises(Exception):
            pyenv_ver_to_travis_ver(v)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
