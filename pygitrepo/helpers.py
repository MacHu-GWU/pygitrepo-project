# -*- coding: utf-8 -*-

try:
    import typing
except:  # pragma: no cover
    pass

import os
import shutil
from re import findall


def split_s3_uri(s3_uri):
    """
    Split AWS S3 URI, returns bucket and key.

    :type s3_uri: str
    :rtype: typing.Tuple[str, str]
    """
    parts = s3_uri.split("/")
    bucket = parts[2]
    key = "/".join(parts[3:])
    return bucket, key


def join_s3_uri(bucket, key):
    """
    Join AWS S3 URI from bucket and key.

    :type bucket: str
    :type key: str
    :rtype: str
    """
    return "s3://{}/{}".format(bucket, key)


def s3_key_smart_join(parts, is_dir):
    """
    Note, it assume that there's no such double slack in your path. It ensure
    that there's only one consecutive "/" in the s3 key.

    :type parts: typing.List[str]
    :param parts: list of s3 key path parts, could have "/"

    :type is_dir: bool
    :param is_dir: if True, the s3 key ends with "/". otherwise enforce no
        tailing "/".

    :rtype: str

    Example::

        >>> s3_key_smart_join(parts=["/a/", "b/", "/c"], is_dir=True)
        a/b/c/

        >>> s3_key_smart_join(parts=["/a/", "b/", "/c"], is_dir=False)
        a/b/c
    """
    new_parts = list()
    for part in parts:
        new_parts.extend([chunk for chunk in part.split("/") if chunk])
    key = "/".join(new_parts)
    if is_dir:
        return key + "/"
    else:
        return key


def make_s3_console_url(bucket=None, prefix=None, s3_uri=None):
    """
    Return an AWS Console url that you can use to open it in your browser.

    :type bucket: str
    :type prefix: str
    :type s3_uri: str
    :rtype: str
    """
    if s3_uri is None:
        if (bucket is None) or (prefix is None):
            raise ValueError
        else:
            pass
    else:
        if (bucket is not None) or (prefix is not None):
            raise ValueError
        bucket, prefix = split_s3_uri(s3_uri)

    if prefix.endswith("/"):
        s3_type = "buckets"
    else:
        s3_type = "object"
    return "https://s3.console.aws.amazon.com/s3/{s3_type}/{bucket}?prefix={prefix}".format(
        s3_type=s3_type,
        bucket=bucket,
        prefix=prefix
    )


def s3_uri_to_url(s3_uri):
    """
    Convert a S3 URI to AWS S3 Console url for preview.

    :type s3_uri
    :rtype: str
    """
    bucket, key = split_s3_uri(s3_uri)
    return make_s3_console_url(bucket=bucket, prefix=key)


def ensure_s3_object(s3_key_or_uri):
    """
    Raise exception if the string is not in valid format for a AWS S3 object
    """
    if s3_key_or_uri.endswith("/"):
        raise ValueError("'{}' doesn't represent s3 object!".format(s3_key_or_uri))


def ensure_s3_dir(s3_key_or_uri):
    """
    Raise exception if the string is not in valid format for a AWS S3 directory
    """
    if not s3_key_or_uri.endswith("/"):
        raise ValueError("'{}' doesn't represent s3 dir!".format(s3_key_or_uri))


def strip_comment_line_with_symbol(line, start):  # pragma: no cover
    """
    Strip comments from line string.
    """
    parts = line.split(start)
    counts = [len(findall(r'(?:^|[^"\\]|(?:\\\\|\\")+)(")', part))
              for part in parts]
    total = 0
    for nr, count in enumerate(counts):
        total += count
        if total % 2 == 0:
            return start.join(parts[:nr + 1]).rstrip()
    else:  # pragma: no cover
        return line.rstrip()


def strip_comments(string, comment_symbols=frozenset(('#', '//'))):  # pragma: no cover
    """
    Strip comments from json string.

    :param string: A string containing json with comments started by comment_symbols.
    :param comment_symbols: Iterable of symbols that start a line comment (default # or //).
    :return: The string with the comments removed.
    """
    lines = string.splitlines()
    for k in range(len(lines)):
        for symbol in comment_symbols:
            lines[k] = strip_comment_line_with_symbol(lines[k], start=symbol)
    return '\n'.join(lines)


def remove_if_exists(abspath):
    """
    Remove a file or a directory (and it's files) if exists.

    :type abspath: str
    """
    if not os.path.exists(abspath):
        return
    if os.path.isdir(abspath):
        shutil.rmtree(abspath)
    else:
        os.remove(abspath)


def makedir_if_not_exists(abspath):
    """
    Make a directory and all required parent folder if not exists.

    :type abspath: str
    """
    if os.path.exists(abspath):
        return
    os.makedirs(abspath)


def copy_python_code(from_dir, to_dir):
    """
    Copy all python source code from one directory to another. Skip
    ``__pycache__``, ``.pyc`` and ``.pyo`` files.

    :type from_dir: str
    :type to_dir: str
    """
    remove_if_exists(to_dir)
    pycache = "__pycache__"
    for dirname, _, basename_list in os.walk(from_dir):
        relpath = os.path.relpath(dirname, from_dir)
        target_dir = os.path.abspath(os.path.join(to_dir, relpath))
        if target_dir.endswith(pycache):
            continue
        else:
            makedir_if_not_exists(target_dir)
        for basename in basename_list:
            # ignore .pyc, the compiled byte code
            # and .pyo, the optimized import cache
            if basename.endswith(".pyc") or basename.endswith(".pyo"):
                continue
            else:
                source_path = os.path.join(dirname, basename)
                target_path = os.path.join(target_dir, basename)
                shutil.copyfile(source_path, target_path)
