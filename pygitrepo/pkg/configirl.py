# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright 2019 Sanhe Hu <https://github.com/MacHu-GWU/configirl-project>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This is a python config management tool to manage config parameter in
centralized place. The purpose of this tool is to avoid maintain complex
config/paramater handling logic in shell script, cloudformation, terraform
and any other devops tools. Instead, we manage that in Python.

Since Python is a full featured general programming language and it is
available on any Mac / Linux machine.

It allows different DevOps tools to easily talk to each other via JSON.

This library implemented in pure Python with no dependencies.
"""

from __future__ import print_function

__version__ = "0.0.10"
__short_description__ = "Centralized Config Management Tool."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

import os
import re
import sys
import json
import copy
import string
import inspect
from collections import OrderedDict
import argparse
import importlib

if sys.version_info.major >= 3 and sys.version_info.minor >= 5:  # pragma: no cover
    import typing


def strip_comment_line_with_symbol(line, start):
    """
    Strip comments from line string.
    """
    parts = line.split(start)
    counts = [len(re.findall(r'(?:^|[^"\\]|(?:\\\\|\\")+)(")', part))
              for part in parts]
    total = 0
    for nr, count in enumerate(counts):
        total += count
        if total % 2 == 0:
            return start.join(parts[:nr + 1]).rstrip()
    else:  # pragma: no cover
        return line.rstrip()


def strip_comments(string, comment_symbols=frozenset(('#', '//'))):
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


def read_text(abspath, encoding="utf-8"):
    """
    Read string from a file.

    :type abspath: str
    :type encoding: str
    :rtype: str
    """
    with open(abspath, "rb") as f:
        return f.read().decode(encoding)


def write_text(text, abspath, encoding="utf-8"):
    """
    Write string to a file.

    :type text: str
    :type abspath: str
    :type encoding: str
    """
    with open(abspath, "wb") as f:
        return f.write(text.encode(encoding))


def json_loads(text):
    """
    Load data from json, ignoring comments.

    :rtype: dict
    """
    return json.loads(strip_comments(text))


def json_dumps(data):
    """
    Dump data to string.

    :rtype: str
    """
    return json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)


def json_load(path):  # pragma: no cover
    """
    Load data from a json file, ignoring comments.

    :type path: str
    """
    with open(path, "rb") as f:
        return json_loads(f.read().decode("utf-8"))


def json_dump(data, path, overwrite=False):  # pragma: no cover
    """
    Dump data to a json file.

    :type data: dict
    :type path: str
    :type overwrite: bool
    """
    if not overwrite:
        if os.path.exists(path):
            raise EnvironmentError("%s already exists!" % path)
    with open(path, "wb") as f:
        f.write(json_dumps(data).encode("utf-8"))


def add_metaclass(metaclass):  # pragma: no cover
    """
    Class decorator for creating a class with a metaclass.

    This method is copied from six.py
    """

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        if hasattr(cls, '__qualname__'):
            orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


try:
    # python3 renamed copy_reg to copyreg
    import copyreg
except ImportError:  # pragma: no cover
    import copy_reg as copyreg


class Sentinel(object):  # pragma: no cover
    _existing_instances = {}

    def __init__(self, name):
        super(Sentinel, self).__init__()
        self._name = name
        self._existing_instances[self._name] = self

    def __repr__(self):
        return "<{0}>".format(self._name)

    def __getnewargs__(self):
        return (self._name,)

    def __new__(cls, name, obj_id=None):  # obj_id is for compatibility with previous versions
        existing_instance = cls._existing_instances.get(name)
        if existing_instance is not None:
            return existing_instance
        return super(Sentinel, cls).__new__(cls)


# obj_id is for compat. with prev. versions
def _sentinel_unpickler(name, obj_id=None):
    if name in Sentinel._existing_instances:
        return Sentinel._existing_instances[name]
    return Sentinel(name)


def _sentinel_pickler(sentinel):
    return _sentinel_unpickler, sentinel.__getnewargs__()


copyreg.pickle(Sentinel, _sentinel_pickler, _sentinel_unpickler)

NOTHING = Sentinel("NOTHING")
REQUIRED = Sentinel("REQUIRED")
OPTIONAL = Sentinel("OPTIONAL")


# --- Exception Class
class ValueNotSetError(Exception):
    """
    Raises when trying to get value of a field that have not set value before.
    """
    pass


class DerivableSetValueError(Exception):
    """
    Raises when trying to set value for Derivable Field.
    """
    pass


# --- Field Class
class Field(object):
    """
    Base class for config value field.

    :type default: typing.Any
    :param default: default value for this field.

    :type dont_dump: bool
    :param dont_dump: if true, then you can't get the value if ``check_dont_dump = True``
        in :meth:`BaseConfigClass.to_dict` and :meth:`BaseConfigClass.to_json`.
        **this prevent from writing sensitive information to file**.

    :type printable: bool
    :param printable: if False, then it will not be displayed with print function.
        **this prevent from displaying sensitive information to the console**.

    :type cache: bool
    :param cache: A flag indicates that whether the cache is enabled.
        only available for :class:`Derivable` if True,
        **then it will cache computation expensive derived value**.
    """
    _creation_index = 0

    def __init__(self,
                 default=NOTHING,
                 dont_dump=False,
                 printable=True,
                 cache=False):
        # name will be update in ConfigMeta meta class.
        self.name = NOTHING
        if callable(default):
            self._value = default()
        else:
            self._value = default
        self.dont_dump = dont_dump  # type: bool
        self.printable = printable  # type: bool
        self.cache = cache  # type: bool

        # _config_object stores the Config object associated with this field
        self._config_object = NOTHING  # type: BaseConfigClass
        # _creation_index used to sort declared fields
        self._creation_index = Field._creation_index  # type: int
        Field._creation_index += 1
        # decorator
        self._getter_method = NOTHING  # type: callable

    def __repr__(self):
        return "{}(name={!r}, value={!r})".format(self.__class__.__name__, self.name, self._value)

    def set_value(self, value):
        """
        An abstract method that set value to this field.
        """
        raise NotImplementedError

    def _get_value(self, **kwargs):
        """
        An abstract method that defines get-value logic flow.
        """
        raise NotImplementedError

    def get_value(self,
                  check_dont_dump=False,
                  check_printable=False,
                  **kwargs):
        """
        Returns the value for this field.

        :type check_dont_dump: bool
        :param check_dont_dump:

        :type check_printable: bool
        :param check_printable:
        :return:

        **CN Doc**

        对于 Constant Field:

        - 如果: self.value = NOTHING, 同时 .set_value(...) 方法从来没有被调用过.
        - 如果: self.value 不等于 NOTHING, 说明 .set_value(...) 方法被吊用过, 则
            返回 self.value

        对于 Derivable Field:

        - 如果: self._getter_method() 没有成功
        """
        if self._config_object is NOTHING:
            raise AttributeError("Field.get_value() can't be called without "
                                 "initialized.")
        if check_dont_dump:
            if self.dont_dump:
                raise DontDumpError(
                    "doesn't allow to dump `{}` field".format(self.name))
        if check_printable:
            if not self.printable:
                return "***HIDDEN***"

        return self._get_value(**kwargs)

    def get_value_from_env(self, prefix=""):
        """
        Use config value stored in environment variables. This usually used
        for computation server that doesn't come with the config file. Since
        config file with sensitive information may not easy to manage. A common
        use case is AWS Lambda Function.

        :param prefix: a prefix append left to the config field name. For exmaple,
            if the config field is ``PROJECT_NAME``, and the prefix is ``MY_PROJECT_``,
            then it will read value from ``MY_PROJECT_PROJECT_NAME``.
        """
        return os.environ[prefix + self.name]

    def get_value_for_lbd(self, prefix=""):
        """
        Smartly decide where should read config value from.
        """
        if self._config_object.is_aws_lambda_runtime():
            return self.get_value_from_env(prefix=prefix)
        else:
            return self.get_value()

    def _validate_method(self, config_object, value):
        return True

    def validator(self, method):
        """
        A decorator to bind validate method.

        :type method: callable
        :param method: a callable function like ``method(self, value)``
            that take ``self`` as first parameters representing the config object.
            ``value`` as second parameters to represent the value you want to validate.
        """
        self._validate_method = method

    def validate(self, *args, **kwargs):
        """
        An abstract method executes the validator method.
        """
        self._validate_method(self._config_object, self.get_value())


class DontDumpError(Exception):
    """
    Raises when trying to dump a ``dont_dump=True`` config value.
    """
    pass


class Constant(Field):
    """
    Constant Value Field.
    """

    def set_value(self, value):
        """
        Set value to this Constant field.
        """
        self._value = value

    def _get_value(self, **kwargs):
        """
        Constant field get-value logic flow.

        If ``self._value`` is ``NOTHING``, it meas the .set_value(...) method
        never be called. Otherwise, return the ``self._value``
        """
        if self._value is NOTHING:
            raise ValueNotSetError(
                "{}.{} has not set a value yet!".format(
                    self._config_object.__class__.__name__, self.name
                )
            )
        return self._value


class Derivable(Field):
    """
    Derivable Value Field.
    """

    def set_value(self, value):
        """
        Derivable field doesn't allow to set value manually!
        """
        raise DerivableSetValueError(
            "{} is a Derivable field, you cannot set value to it".format(
                self.name
            ))

    def getter(self, method):
        """
        A decorator to bind getter method.
        """
        self._getter_method = method

    def _get_value(self, **kwargs):
        """
        Derivable field get-value logic flow.

        If ``self._getter_method`` is ``NOTHING``, it means the getter method
        is not implemented yet.

        If cache is enabled, try to retrieve value from existing value stored in
        ``self._value``. If not available, call the getter method to retrieve
        the value.

        If cache is disabled, call the getter method.
        """
        if self._getter_method is NOTHING:
            raise NotImplementedError(
                "{}.{} getter method is not implemented, "
                "use @{}.getter to decorate a getter function.".format(
                    self._config_object.__class__.__name__, self.name, self.name
                ))

        try:
            if self.cache:
                if self._value is NOTHING:
                    self._value = self._getter_method(
                        self._config_object, **kwargs)
                return self._value
            else:
                return self._getter_method(self._config_object, **kwargs)
        except ValueNotSetError as e:  # dependent constant value not set yet
            raise ValueNotSetError(
                "can't get {}.{}, because: {}".format(
                    self._config_object.__class__.__name__, self.name, e
                )
            )
        except Exception as e:
            raise e


def is_instance_or_subclass(val, class_):
    """Return True if ``val`` is either a subclass or instance of ``class_``."""
    try:
        return issubclass(val, class_)
    except TypeError:
        return isinstance(val, class_)


def _get_fields(attrs, field_class, pop=False, ordered=False):
    """Get fields from a class. If ordered=True, fields will sorted by creation index.

    :param attrs: Mapping of class attributes
    :param type field_class: Base field class
    :param bool pop: Remove matching fields
    """
    fields = [
        (field_name, field_value)
        for field_name, field_value in attrs.items()
        if is_instance_or_subclass(field_value, field_class)
    ]
    if pop:  # pragma: no cover
        for field_name, _ in fields:
            del attrs[field_name]
    if ordered:
        fields.sort(key=lambda pair: pair[1]._creation_index)
    return fields


def _get_fields_by_mro(klass, field_class, ordered=False):
    """
    Collect fields from a class, following its method resolution order. The
    class itself is excluded from the search; only its parents are checked. Get
    fields from ``_declared_fields`` if available, else use ``__dict__``.

    :param type klass: Class whose fields to retrieve
    :param type field_class: Base field class
    """
    mro = inspect.getmro(klass)
    # Loop over mro in reverse to maintain correct order of fields
    return sum(
        (
            _get_fields(
                getattr(base, "_declared_fields", base.__dict__),
                field_class,
                ordered=ordered,
            )
            for base in mro[:0:-1]
        ),
        [],
    )


VALID_CHAR_SET = set(string.ascii_uppercase + string.digits + "_")


def _validate_field_name(field_name):
    """
    Validate config field name naming convention. Only [A-Z0-9_] is allowed.
    lowercase is not allowed.
    """
    if len(set(field_name).difference(VALID_CHAR_SET)):
        msg = "'{}' is not a valid field name, only [A-Z0-9_] is allowed!" \
            .format(field_name)
        raise ValueError(msg)


class ConfigMeta(type):
    """
    Config class meta class. Collect declared :class:`Field`, assign field name.
    """

    def __new__(cls, name, bases, attrs):
        cls_fields = _get_fields(attrs, Field, pop=False, ordered=True)
        klass = super(ConfigMeta, cls).__new__(cls, name, bases, attrs)
        inherited_fields = _get_fields_by_mro(klass, Field, ordered=True)

        # Assign _declared_fields on class
        klass._declared_fields = OrderedDict(inherited_fields + cls_fields)
        klass._constant_fields = OrderedDict([
            (name, field)
            for name, field in klass._declared_fields.items()
            if isinstance(field, Constant)
        ])
        klass._deriable_fields = OrderedDict([
            (name, field)
            for name, field in klass._declared_fields.items()
            if isinstance(field, Derivable)
        ])
        for name, field in klass._declared_fields.items():
            _validate_field_name(name)
            field.name = name
        return klass


class BaseConfigClass(object):
    """
    Config class base class.

    - :attr:`BaseConfigClass._declared_fields`:
    - :attr:`BaseConfigClass._constant_fields`:
    - :attr:`BaseConfigClass._deriable_fields`:
    """
    _declared_fields = OrderedDict()  # type: typing.Dict[str: Field]
    _constant_fields = OrderedDict()  # type: typing.Dict[str: Constant]
    _deriable_fields = OrderedDict()  # type: typing.Dict[str: Derivable]

    # --- constructor method
    def __init__(self, **kwargs):
        self.__pre_init_hook()
        for name, field in self._declared_fields.items():
            if name in kwargs:
                field.set_value(kwargs[name])

            field._config_object = self

    def __pre_init_hook(self):
        """
        All declared fields is a mutable :class:`Field` Instance, defined
        in Class level. So when you creating a new instance, the class
        level fields have to be deep copied to the config instance.
        """
        self._declared_fields = OrderedDict([
            (attr, copy.deepcopy(field))
            for attr, field in self._declared_fields.items()
        ])
        self._constant_fields = OrderedDict([
            (attr, self._declared_fields[attr])
            for attr, _ in self._constant_fields.items()
        ])
        self._deriable_fields = OrderedDict([
            (attr, self._declared_fields[attr])
            for attr, _ in self._deriable_fields.items()
        ])

        for attr, field in self._declared_fields.items():
            setattr(self, attr, field)

    @classmethod
    def from_dict(cls, dct):
        """
        A factory classmethod construct config object from dict.
        Only loads constant field. If a key is an undefined field,
        it automatically been ignored.

        :type dct: dict
        :rtype: BaseConfigClass
        """
        cfg = cls()
        for key, value in dct.items():
            if key in cfg._constant_fields:
                cfg._constant_fields[key].set_value(value)
        return cfg

    @classmethod
    def from_json_str(cls, json_str):
        """
        A factory classmethod construct config object from json string.
        json string can includes comments.
        Only loads constant field. If a key is an undefined field,
        it automatically been ignored.

        :type json_str: str
        :rtype: BaseConfigClass
        """
        return cls.from_dict(json_loads(json_str))

    @classmethod
    def from_json_file(cls, json_file):  # pragma: no cover
        """
        A factory classmethod construct config object from a json file.
        json string can includes comments.
        Only loads constant field. If a key is an undefined field,
        it automatically been ignored.

        :type json_file: str
        :rtype: BaseConfigClass
        """
        return cls.from_dict(json_load(json_file))

    @classmethod
    def from_env_var(cls, prefix):  # pragma: no cover
        """
        A factory classmethod construct config object from environment variables.
        Only loads constant field. If a key is an undefined field,
        it automatically been ignored.

        :type json_file: str
        :rtype: BaseConfigClass
        """
        cfg = cls()
        cfg.update_from_env_var(prefix=prefix)
        return cfg

    def update(self, dct):
        """
        Update constant config values from a dictionary.
        Only those fields defines as Constant value will be loaded.
        If a key is an undefined field, it automatically been ignored.

        :type dct: dict
        :rtype: dict
        :return: loaded data
        """
        loaded_data = dict()
        for key, value in dct.items():
            if key in self._constant_fields:
                self._constant_fields[key].set_value(value)
                loaded_data[key] = value
        return loaded_data

    def update_from_raw_json_file(self):
        """
        Update constant config values from the :attr:`BaseConfigClass.CONFIG_RAW_JSON_FILE`.

        :rtype: dict
        :return: loaded data
        """
        dct = json_load(self.CONFIG_RAW_JSON_FILE)
        return self.update(dct)

    def update_from_env_var(self, prefix):
        """
        Update constant config values from environment variables.

        :type prefix: str
        :param prefix: a prefix used in all related environment variable.

        :rtype: dict
        :return: loaded data
        """
        dct = {
            key.replace(prefix, "", 1): value
            for key, value in os.environ.items()
            if key.replace(prefix, "", 1)
        }
        self.update(dct)
        return dct

    def to_dict(self,
                check_dont_dump=True,
                check_printable=False,
                ignore_na=False,
                prefix=""):
        """
        Dump config values to dictionary.

        :type check_dont_dump: bool
        :param check_dont_dump: if True, then it will check if a field has
            a True value ``dont_dump`` flag, then :class:`DontDumpError` error
            is raised.

        :type check_printable: bool
        :param check_printable: if True, then it will check if a field has
            a False value ``printable`` flag, then it returns **HIDDEN**.

        :type ignore_na: bool
        :param ignore_na: if True, then :class:`ValueNotSetError` error will be
            ignored.

        :type prefix: str
        :param prefix: a prefix that appended to the left of every field

        :rtype: dict
        """
        dct = OrderedDict()
        for attr, value in self._declared_fields.items():
            key = prefix + attr
            try:
                dct[key] = value.get_value(
                    check_dont_dump=check_dont_dump,
                    check_printable=check_printable,
                )
            except DontDumpError:
                pass
            except ValueNotSetError as e:
                if ignore_na:
                    pass
                else:
                    raise e
            except Exception as e:
                raise e
        return dct

    def to_json(self,
                check_dont_dump=True,
                check_printable=False,
                ignore_na=False,
                prefix=""):
        """
        Dump config values to json.

        :type check_dont_dump: bool
        :param check_dont_dump: if True, then it will check if a field has
            a True value ``dont_dump`` flag, then :class:`DontDumpError` error
            is raised.

        :type check_printable: bool
        :param check_printable: if True, then it will check if a field has
            a False value ``printable`` flag, then it returns **HIDDEN**.

        :type ignore_na: bool
        :param ignore_na: if True, then :class:`ValueNotSetError` error will be
            ignored.

        :type prefix: str
        :param prefix: a prefix that appended to the left of every field

        :rtype: str
        """
        return json.dumps(
            self.to_dict(
                check_dont_dump=check_dont_dump,
                check_printable=check_printable,
                ignore_na=ignore_na,
                prefix=prefix,
            ),
            indent=4, sort_keys=False,
        )

    def __repr__(self):
        return "Config({})".format(
            self.to_json(check_dont_dump=False, check_printable=True)
        )

    def pprint(self):
        print(self.__repr__())

    def validate(self):
        for field in self._declared_fields.values():
            field.validate()

    # --- Runtime Detection ---
    @classmethod
    def is_aws_ec2_amz_linux_runtime(cls):  # pragma: no cover
        """
        Check whether it is Amazon Linux EC2 runtime.

        :rtype: bool
        """
        if os.environ["HOME"].endswith("ec2-user"):
            return True
        else:
            return False

    @classmethod
    def is_aws_ec2_redhat_runtime(cls):  # pragma: no cover
        """
        Check whether it is RedHat AWS EC2 runtime.

        :rtype: bool
        """
        if os.environ["HOME"].endswith("ec2-user"):
            return True
        else:
            return False

    @classmethod
    def is_aws_ec2_freebsd_runtime(cls):  # pragma: no cover
        """
        Check whether it is FreeBSD AWS EC2 runtime.

        :rtype: bool
        """
        if os.environ["HOME"].endswith("ec2-user"):
            return True
        else:
            return False

    @classmethod
    def is_aws_lambda_runtime(cls):  # pragma: no cover
        """
        Check whether it is Amazon Lambda Function runtime.

        Ref: https://docs.aws.amazon.com/lambda/latest/dg/lambda-environment-variables.html

        :rtype: bool
        """
        if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
            return True
        else:
            return False

    @classmethod
    def is_aws_code_build_runtime(cls):  # pragma: no cover
        """
        Check whether it is AWS Code Build runtime.

        Ref: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html

        :rtype: bool
        """
        if "CODEBUILD_BUILD_ID" in os.environ:
            return True
        else:
            return False

    # CI
    @classmethod
    def is_ci_runtime(cls):  # pragma: no cover
        """
        Check whether it is CI runtime.

        :rtype: bool
        """
        if "CI" in os.environ:
            if os.environ["CI"]:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def is_circle_ci_runtime(cls):  # pragma: no cover
        """
        Check whether it is CircleCI runtime.

        Ref: https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables

        :rtype: bool
        """
        if "CIRCLECI" in os.environ:
            if os.environ["CIRCLECI"]:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def is_travis_ci_runtime(cls):  # pragma: no cover
        """
        Check whether it is TravisCI runtime.

        Ref: https://docs.travis-ci.com/user/environment-variables/#default-environment-variables

        :rtype: bool
        """
        if "TRAVIS" in os.environ:
            if os.environ["TRAVIS"]:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def is_gitlab_ci_runtime(cls):  # pragma: no cover
        """
        Check whether it is GitlabCI runtime.

        Ref: https://docs.gitlab.com/ee/ci/variables/

        :rtype: bool
        """
        if "GITLAB_CI" in os.environ:
            if os.environ["GITLAB_CI"]:
                return True
            else:
                return False
        else:
            return False

    # --- config file path management
    CONFIG_DIR = NOTHING  # type: str

    def _join_config_dir(self, filename):
        if self.CONFIG_DIR is NOTHING:
            raise ValueError("You have to specify `{}.CONFIG_DIR`!".format(
                self.__class__.__name__))
        if not os.path.exists(self.CONFIG_DIR):
            raise ValueError("`{}.CONFIG_DIR` ('{}') doesn't exist!".format(
                self.__class__.__name__, self.CONFIG_DIR))
        return os.path.join(self.CONFIG_DIR, filename)

    @property
    def CONFIG_RAW_JSON_FILE(self):
        return self._join_config_dir("config-raw.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_PYTHON(self):
        return self._join_config_dir("config-final-for-python.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SHELL_SCRIPT(self):
        return self._join_config_dir("config-final-for-shell-script.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_CLOUDFORMATION(self):
        return self._join_config_dir("config-final-for-cloudformation.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SAM(self):
        return self._join_config_dir("config-final-for-sam.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SERVERLESS(self):
        return self._join_config_dir("config-final-for-serverless.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_TERRAFORM(self):
        return self._join_config_dir("config-final-for-terraform.json")

    # --- Custom logic for different devops tools
    def to_python_json_config_data(self):
        return self.to_dict()

    def to_shell_script_config_data(self):
        return self.to_dict()

    def to_cloudformation_config_data(self):
        def to_big_camel_case(text):
            return "".join([
                word[0].upper() + word[1:].lower()
                for word in text.split("_")
            ])

        return OrderedDict([
            (to_big_camel_case(key), value)
            for key, value in self.to_dict().items()
        ])

    def to_sam_config_data(self):
        return self.to_dict()

    def to_serverless_config_data(self):
        return self.to_dict()

    def to_terraform_config_data(self):
        return self.to_dict()

    def _dump_for_xxx_config_file(self,
                                  to_config_data_meth,
                                  config_json_file_path):
        json_str = json_dumps(to_config_data_meth())
        write_text(json_str, config_json_file_path)

    def dump_python_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_python_json_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_PYTHON,
        )

    def dump_shell_script_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_shell_script_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_SHELL_SCRIPT,
        )

    def dump_cloudformation_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_cloudformation_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_CLOUDFORMATION,
        )

    def dump_sam_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_sam_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_SAM,
        )

    def dump_serverless_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_serverless_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_SERVERLESS,
        )

    def dump_terraform_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_terraform_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_TERRAFORM,
        )


@add_metaclass(ConfigMeta)
class ConfigClass(BaseConfigClass):
    pass


# --- Command Line Interface ---

class SubCommands:
    read_json_value = "read-json-value"
    get_config_value = "get-config-value"
    import_config_value = "import-config-value"


def read_json_value(path, field):
    """
    Return a value of a field from a Json file, ignoring the comments
    """
    # find absolute path
    cwd = os.getcwd()

    if not os.path.isabs(path):
        file_path = os.path.abspath(os.path.join(cwd, path))
    else:
        file_path = path

    # fix json_path
    json_path = field
    if json_path.startswith("$."):
        json_path = json_path.replace("$.", "", 1)

    # read data
    with open(file_path, "rb") as f:
        data = json.loads(strip_comments(f.read().decode("utf-8")))

    # access value
    value = data
    for part in json_path.split("."):
        if part in value:
            value = value[part]
        else:
            raise ValueError(
                "'$.{}' not found in {}".format(json_path, file_path))
    return value


def get_config_value(module, field):
    """
    Initialize a Config Class defined in a python module, and get the value
    of a field. The module has to be able to be import.
    """
    chunks = module.split(".")
    module_object = importlib.import_module(".".join(chunks[:-1]))
    klass = getattr(module_object, chunks[-1])
    cfg_obj = klass()
    attribute = getattr(cfg_obj, field)
    if isinstance(attribute, Field):
        return attribute.get_value()
    elif callable(attribute):
        return attribute()
    else:
        return attribute


def import_config_value(sys_path, module, field):
    """
    Initialize a Config Class defined in a python module, and get the value
    of a field. The module has to be able to be import when arg ``sys_path``
    been add to sys.path.
    """
    if sys_path not in sys.path:
        sys.path.append(sys_path)
    return get_config_value(module, field)


parser = argparse.ArgumentParser(
    prog="configirl",
)

subparser = parser.add_subparsers(
    title="sub commands",
    dest="sub_command",
)

read_json_value_parser = subparser.add_parser(
    SubCommands.read_json_value,
    description=(
        "read config value from a json file."
    ),
)
read_json_value_parser.add_argument(
    "--path",
    type=str,
    metavar="path",
    nargs=1,
    help="The json file path",
    required=True,
)
read_json_value_parser.add_argument(
    "--field",
    type=str,
    metavar="field_name",
    nargs=1,
    help="The value of json field you want to access. For example: STAGE",
    required=True,
)

get_config_value_parser = subparser.add_parser(
    SubCommands.get_config_value,
    description=(
        "get config value by importing a Config object from a python module, "
        "and initializing a config object, "
        "and then call ``Config().FIELD_NAME.get_value()`` method."
    ),
)
get_config_value_parser.add_argument(
    "--module",
    type=str,
    metavar="module_name",
    nargs=1,
    help=(
        "The path you want to add to ``sys.path`` that allows python to find your module. "
        "For example: path-to/configirl-project"
    ),
    required=True,
)
get_config_value_parser.add_argument(
    "--field",
    type=str,
    metavar="field_name",
    nargs=1,
    help=(
        "The value of config field you want to access. "
        "For example: ENVIRONMENT_NAME"
    ),
    required=True,
)

import_config_value_parser = subparser.add_parser(
    SubCommands.import_config_value,
    description=(
        "import config value by importing a Config object from a python module, "
        "where locate at custom system path, "
        "and initializing a config object, "
        "and then call ``Config().FIELD_NAME.get_value()`` method."
    ),
)
import_config_value_parser.add_argument(
    "--sys_path",
    type=str,
    metavar="sys_path",
    nargs=1,
    help=(
        "The path you want to add to ``sys.path`` that allows python to find your module. "
        "For example: path-to/configirl-project"
    ),
    required=True,
)
import_config_value_parser.add_argument(
    "--module",
    type=str,
    metavar="module_name",
    nargs=1,
    help=(
        "The config class module name. "
        "For example: configirl.tests.config.Config"
    ),
    required=True,
)
import_config_value_parser.add_argument(
    "--field",
    type=str,
    metavar="field_name",
    nargs=1,
    help=(
        "The value of config field you want to access. "
        "For example: ENVIRONMENT_NAME"
    ),
    required=True,
)


def main():  # pragma: no cover
    """
    Command Line Interface entry point.
    """
    args = parser.parse_args()
    if args.sub_command == SubCommands.read_json_value:
        print(read_json_value(path=args.path[0], field=args.field[0]))
    elif args.sub_command == SubCommands.get_config_value:
        print(get_config_value(module=args.module[0], field=args.field[0]))
    elif args.sub_command == SubCommands.import_config_value:
        print(import_config_value(
            sys_path=args.sys_path[0], module=args.module[0], field=args.field[0]))
    else:
        raise NotImplementedError
