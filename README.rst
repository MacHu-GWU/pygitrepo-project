.. image:: https://travis-ci.org/MacHu-GWU/pygitrepo-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/pygitrepo-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/pygitrepo-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/pygitrepo-project

.. image:: https://img.shields.io/pypi/v/pygitrepo.svg
    :target: https://pypi.python.org/pypi/pygitrepo

.. image:: https://img.shields.io/pypi/l/pygitrepo.svg
    :target: https://pypi.python.org/pypi/pygitrepo

.. image:: https://img.shields.io/pypi/pyversions/pygitrepo.svg
    :target: https://pypi.python.org/pypi/pygitrepo

.. image:: https://img.shields.io/badge/Star_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/pygitrepo-project


Welcome to ``pygitrepo`` Documentation
==============================================================================

``pygitrepo`` can quickly initiate a python project from scratch, with these **powerful tools** out-of-the-box:

- ``make up``: single command to create/clean virtual environment.
- ``make reformat``: command to Google stylize your code.
- ``make install``: install your package (``setup.py`` file is out-of-the-box).
- ``make test``: unittest with `pytest <https://pypi.python.org/pypi/pytest>`_ (tests folder and scripts is out-of-the-box, just follow the pattern and create more).
- ``make cov``: code coverage test with `coverage <https://pypi.python.org/pypi/coverage>`_, the default ``.coveragerc`` fit most of the case).
- ``make tox``: multi python version test with tox, the default ``tox.ini`` fit most of the case.
- built-in integration with https://travis-ci.org/.
- built-in integration with https://codecov.io/.
- ``make build_doc / view_doc``: easy sphinx document writing, no need to run ``sphinx-quickstart``, and write ``conf.py`` file.
- ``make deploy_doc``: deploy document to `AWS S3 <http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_.
- ``make publish``: publish your project to `PyPI <https://pypi.python.org/pypi>`_


``pygitrepo`` is compatible with Windows / MacOS / Linux.


Quick Links
-----------

- .. image:: https://img.shields.io/badge/Link-Document-red.svg
      :target: http://www.wbh-doc.com.s3.amazonaws.com/pygitrepo/index.html

- .. image:: https://img.shields.io/badge/Link-API_Reference_and_Source_Code-red.svg
      :target: API reference and source code <http://www.wbh-doc.com.s3.amazonaws.com/pygitrepo/py-modindex.html

- .. image:: https://img.shields.io/badge/Link-Install-red.svg
      :target: `install`_

- .. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/pygitrepo-project

- .. image:: https://img.shields.io/badge/Link-Submit_Issue_and_Feature_Request-blue.svg
      :target: https://github.com/MacHu-GWU/pygitrepo-project/issues

- .. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.python.org/pypi/pygitrepo#downloads


Usage
-----
1. Install: ``pip install pygitrepo``.
2. Run command line tool: ``pygitrepo-init``.
3. A ``<repo-name>`` directory will be created, you can use this as your github repo directory.
4. Take a look at ``Makefile``, all magic happens here!


Things Need to Install
------------------------------------------------------------------------------


For Windows (Git-Bash and MinGW)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Because Windows doesn't have ``shell script`` and ``make`` command, so we have to install some third-party software to make it works.

**Install Git Bash as shell emulator**

1. `Download and install git <https://git-scm.com/downloads>`_.
2. Now you can use ``C:\Program Files\Git\git-bash.exe`` like the terminal in MacOS/Linux.

**Install MinGW**

1. `Download and install <http://www.mingw.org/>`_, use the installer to install ``MinGW Base``.
2. Find ``C:\MinGW\bin\mingw32-make.exe``, copy and paste and rename as ``C:\MinGW\bin\make.exe``.
3. Add ``C:\MinGW\bin`` to $PATH (environment variable).

Now you can use ``make <target>`` in ``git-bash.exe`` now.


For MacOS (HomeBrew)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You have to make sure:

- `HomeBrew <https://brew.sh/>`_ is installed.

There's two way of using virtualenv in MacOS:

1. Use generic `virtualenv <https://virtualenv.pypa.io/en/stable/>`_.
2. Use `pyenv <https://github.com/pyenv/pyenv>`_ + `pyenv-virtualenv <https://github.com/pyenv/pyenv-virtualenv>`_.

I prefer ``pyenv`` + ``pyenv-virtualenv``, because it allows you:

1. use tox to test against multiple python version locally before using cloud CI (continues integration).
2. will not mess up your global python environment.
3. the ``Makefile`` will do the ``pyenv`` + ``pyenv-virtualenv`` setup for you, just make sure that you have  `HomeBrew <https://brew.sh/>`_ installed.



AWS Command Line (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use `AWS S3 <http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ to host your doc site is a good idea!

We need `awscli <https://aws.amazon.com/cli/>`_ to automate the deployment.

1. Install `awscli <https://aws.amazon.com/cli/>`_, just ``pip install awscli``.
2. `Configure your API token <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html>`_, just ``aws configure`` and follow the instruction.


Config PyPI (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to publish your package to `PyPI <https://pypi.python.org/pypi>`_ or `new PyPI <https://pypi.org/>`_, you need a pypi account and `Configure your credential <https://docs.python.org/2/distutils/packageindex.html#pypirc>`_.

1. Create a ``${HOME}/.pypirc`` file.
2. put these contents::

    [distutils]
    index-servers =
        pypi

    [pypi]
    username:<username>
    password:<password>


CI (Continues Integration) (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. `Test with travis-ci <https://docs.travis-ci.com/user/languages/python/>`_, basically you just need to:
    - sign in using GitHub account.
    - toggle on your repo.
2. `Code Coverage Test with codecov <https://github.com/codecov/example-python>`_.


.. _install:

Install
-------

``pygitrepo`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install pygitrepo

To upgrade to latest version:

.. code-block:: console

	$ pip install --upgrade pygitrepo