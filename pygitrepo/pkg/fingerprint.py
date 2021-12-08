# -*- coding: utf-8 -*-

"""
This module is built on Python standard hashlib, provides utility method
to find hash value for a bytes, a string, a Python object or a file.
Import this module::

    >>> from fingerprint import fingerprint

Example::

    >>> fingerprint.of_bytes(bytes(16))
    >>> fingerprint.of_text("Hello World")
    >>> fingerprint.of_pyobj(dict(a=1, b=2, c=3))
    >>> fingerprint.of_file("fingerprint.py")

You can switch the hash algorithm to use::

    >>> fingerprint.use("md5") # also "sha1", "sha256", "sha512"

**中文文档**

本模块提供了一些计算Hash值的简便方法。对于 of_pyobj()方法来说, 请注意在读写时
均使用相同的Python大版本(2/3)。
"""

from pygitrepo.pkg.mini_six import PY2, PY3, text_type, binary_type
import pickle
import hashlib

if PY2:  # pragma: no cover
    default_pk_protocol = 2
elif PY3:  # pragma: no cover
    default_pk_protocol = 2


class FingerPrint(object):
    """A hashlib wrapper class allow you to use one line to do hash as you wish.
    :type algorithm: str
    :param algorithm: default "md5"
    Usage::
        >>> from pygitrepo.fingerprint import fingerprint
        >>> print(fingerprint.of_bytes(bytes(123)))
        b1fec41621e338896e2d26f232a6b006
        >>> print(fingerprint.of_text("message"))
        78e731027d8fd50ed642340b7c9a63b3
        >>> print(fingerprint.of_pyobj({"key": "value"}))
        4c502ab399c89c8758a2d8c37be98f69
        >>> print(fingerprint.of_file("fingerprint.py"))
        4cddcb5562cbff652b0e4c8a0300337a
    """
    _mapper = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }

    def __init__(self, algorithm="md5", pk_protocol=default_pk_protocol):
        self.hash_algo = hashlib.md5
        self.return_int = False
        self.pk_protocol = 2

        self.use(algorithm)
        self.set_return_str()
        self.set_pickle_protocol(pk_protocol)

    def use(self, algorithm):
        """Change the hash algorithm you gonna use.
        """
        try:
            self.hash_algo = self._mapper[algorithm.strip().lower()]
        except IndexError:  # pragma: no cover
            template = "'%s' is not supported, try one of %s."
            raise ValueError(template % (algorithm, list(self._mapper)))

    def use_md5(self):
        """
        Use md5 hash algorithm.
        """
        self.use("md5")

    def use_sha1(self):
        """
        Use sha1 hash algorithm.
        """
        self.use("sha1")

    def use_sha256(self):
        """
        Use sha256 hash algorithm.
        """
        self.use("sha256")

    def use_sha512(self):
        """
        Use sha512 hash algorithm.
        """
        self.use("sha512")

    def digest_to_int(self, digest):
        """Convert hexdigest str to int.
        """
        return int(digest, 16)

    def set_return_int(self):
        """Set to return hex integer.
        """
        self.return_int = True

    def set_return_str(self):
        """Set to return hex string.
        """
        self.return_int = False

    def set_pickle_protocol(self, pk_protocol):
        """Set pickle protocol.
        """
        if pk_protocol not in [2, 3]:
            raise ValueError("pickle protocol has to be 2 or 3!")
        self.pk_protocol = pk_protocol

    def set_pickle2(self):
        """
        Set pickle protocol to 2.
        """
        self.set_pickle_protocol(2)

    def set_pickle3(self):
        """
        Set pickle protocol to 3.
        """
        self.set_pickle_protocol(3)

    def digest(self, hash_method):
        if self.return_int:
            return int(hash_method.hexdigest(), 16)
        else:
            return hash_method.hexdigest()

    # hash function
    def of_bytes(self, py_bytes):
        """
        Use default hash method to return hash value of bytes.
        :type py_bytes: binary_type
        :param py_bytes: a binary object
        """
        m = self.hash_algo()
        m.update(py_bytes)
        return self.digest(m)

    def of_text(self, text, encoding="utf-8"):
        """
        Use default hash method to return hash value of a piece of string
        default setting use 'utf-8' encoding.
        :type text: text_type
        :param text: a text object
        """
        m = self.hash_algo()
        m.update(text.encode(encoding))
        return self.digest(m)

    def of_pyobj(self, pyobj):
        """
        Use default hash method to return hash value of a piece of Python
        picklable object.
        :param pyobj: any python object
        """
        m = self.hash_algo()
        m.update(pickle.dumps(pyobj, protocol=self.pk_protocol))
        return self.digest(m)

    def of_file(self, abspath, nbytes=0, chunk_size=1024):
        """
        Use default hash method to return hash value of a piece of a file
        Estimate processing time on:
        :type abspath: text_type
        :param abspath: the absolute path to the file.
        :type nbytes: int
        :param nbytes: only has first N bytes of the file. if 0, hash all file.
        :type chunk_size: int
        :param chunk_size: The max memory we use at one time.
        CPU = i7-4600U 2.10GHz - 2.70GHz, RAM = 8.00 GB
        1 second can process 0.25GB data
        - 0.59G - 2.43 sec
        - 1.3G - 5.68 sec
        - 1.9G - 7.72 sec
        - 2.5G - 10.32 sec
        - 3.9G - 16.0 sec
        ATTENTION:
            if you change the meta data (for example, the title, years
            information in audio, video) of a multi-media file, then the hash
            value gonna also change.
        """
        if nbytes < 0:
            raise ValueError("chunk_size cannot smaller than 0")
        if chunk_size < 1:
            raise ValueError("chunk_size cannot smaller than 1")
        if (nbytes > 0) and (nbytes < chunk_size):
            chunk_size = nbytes

        m = self.hash_algo()
        with open(abspath, "rb") as f:
            if nbytes:  # use first n bytes
                have_reads = 0
                while True:
                    have_reads += chunk_size
                    if have_reads > nbytes:
                        n = nbytes - (have_reads - chunk_size)
                        if n:
                            data = f.read(n)
                            m.update(data)
                        break
                    else:
                        data = f.read(chunk_size)
                        m.update(data)
            else:  # use entire content
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    m.update(data)

        return m.hexdigest()


fingerprint = FingerPrint()
