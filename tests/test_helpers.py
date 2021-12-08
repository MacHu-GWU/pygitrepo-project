# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import pytest
from pygitrepo.helpers import (
    split_s3_uri,
    join_s3_uri,
    s3_key_smart_join,
    make_s3_console_url,
    remove_if_exists,
    makedir_if_not_exists,
)

dir_here = os.path.dirname(os.path.abspath(__file__))


def test_split_s3_uri():
    s3_uri = "s3://my-bucket/my-prefix/my-file.zip"
    bucket, key = split_s3_uri(s3_uri)
    assert bucket == "my-bucket"
    assert key == "my-prefix/my-file.zip"


def test_join_s3_uri():
    bucket = "my-bucket"
    key = "my-prefix/my-file.zip"
    s3_uri = join_s3_uri(bucket, key)
    assert s3_uri == "s3://my-bucket/my-prefix/my-file.zip"


def test_s3_key_smart_join():
    assert s3_key_smart_join(
        parts=["/a/", "b/", "/c"], is_dir=True) == "a/b/c/"
    assert s3_key_smart_join(
        parts=["/a/", "b/", "/c"], is_dir=False) == "a/b/c"


def test_make_s3_console_url():
    url = make_s3_console_url("my-bucket", "my-file.zip")
    assert "object" in url

    url = make_s3_console_url("my-bucket", "my-folder/")
    assert "bucket" in url


def test_remove_if_exists():
    p = os.path.join(dir_here, "tmp")
    remove_if_exists(p)
    assert os.path.exists(p) is False

    makedir_if_not_exists(p)
    assert os.path.exists(p) is True

    remove_if_exists(p)
    assert os.path.exists(p) is False


def test_makedir_if_not_exists():
    p = os.path.join(dir_here, "tmp")
    remove_if_exists(p)
    assert os.path.exists(p) is False

    makedir_if_not_exists(p)
    makedir_if_not_exists(p)
    assert os.path.exists(p) is True

    remove_if_exists(p)
    assert os.path.exists(p) is False


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
