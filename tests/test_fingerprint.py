# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest
from pygitrepo.pkg.fingerprint import fingerprint
from pygitrepo.pkg.mini_six import integer_types, string_types


def test_md5_file():
    fingerprint.use_md5()
    fingerprint.set_return_str()
    fingerprint.set_pickle2()

    a_file = __file__.replace("test_fingerprint.py", "all.py")

    id1 = fingerprint.of_file(a_file)
    id2 = fingerprint.of_file(a_file, nbytes=1000)
    id3 = fingerprint.of_file(a_file, chunk_size=1)
    id4 = fingerprint.of_file(a_file, chunk_size=2)
    assert id1 == id2 == id3 == id4

    id1 = fingerprint.of_file(a_file, nbytes=5)
    id2 = fingerprint.of_file(a_file, nbytes=5, chunk_size=2)
    id3 = fingerprint.of_file(a_file, nbytes=5, chunk_size=1)
    assert id1 == id2 == id3

    with pytest.raises(ValueError) as exc_info:
        fingerprint.of_file(a_file, nbytes=-1)

    with pytest.raises(ValueError) as exc_info:
        fingerprint.of_file(a_file, chunk_size=0)


def test_hash_anything():
    """This test may failed in different operation system.
    """
    fingerprint.use_md5()
    fingerprint.set_return_str()
    fingerprint.set_pickle2()

    a_bytes = bytes(123)
    md5 = fingerprint.of_bytes(a_bytes)
    assert isinstance(md5, string_types)

    a_text = "Hello World!"
    md5 = fingerprint.of_bytes(a_bytes)
    assert isinstance(md5, string_types)

    a_pyobj = {"key": "value"}
    md5 = fingerprint.of_pyobj(a_pyobj)
    assert isinstance(md5, string_types)

    fingerprint.set_return_int()
    assert isinstance(fingerprint.of_text(a_text), integer_types)
    fingerprint.set_return_str()


def test_basic_function():
    a_bytes = "Hello World!".encode("utf-8")
    a_text = "Hello World!"
    a_pyobj = {"key": "value"}
    a_file = __file__.replace("test_fingerprint.py", "all.py")

    use_method_list = [
        fingerprint.use_md5,
        fingerprint.use_sha1,
        fingerprint.use_sha256,
        fingerprint.use_sha512,
    ]
    for use_method in use_method_list:
        use_method()
        fingerprint.of_bytes(a_bytes)
        fingerprint.of_text(a_text)
        fingerprint.of_pyobj(a_pyobj)
        fingerprint.of_file(a_file)


def test_int_digest():
    a_text = "Hello World!"
    fingerprint.set_return_int()
    assert isinstance(fingerprint.of_text(a_text), integer_types)


def test_set_lots_of_mode():
    fingerprint.set_return_int()
    fingerprint.set_return_str()
    fingerprint.set_pickle2()
    fingerprint.set_pickle3()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
