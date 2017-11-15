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

``pygitrepo`` can quickly initiate a python project from scratch, and you get these development tools ready to use and configured:

- virtual environment management, **up, clean, switch**.
- continues integration for **unit test and code coverage** on your **local machine** and **also cloud**.
- document site management, **write, build, view and deploy**.
- **publish your package to PyPI**, make it installable everywhere.


Quick Links
------------------------------------------------------------------------------

- .. image:: https://img.shields.io/badge/Link-Document-red.svg
      :target: https://pygitrepo.readthedocs.io/index.html

- .. image:: https://img.shields.io/badge/Link-API_Reference_and_Source_Code-red.svg
      :target: https://pygitrepo.readthedocs.io/py-modindex.html

- .. image:: https://img.shields.io/badge/Link-Install-red.svg
      :target: `install`_

- .. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/pygitrepo-project

- .. image:: https://img.shields.io/badge/Link-Submit_Issue_and_Feature_Request-blue.svg
      :target: https://github.com/MacHu-GWU/pygitrepo-project/issues

- .. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.python.org/pypi/pygitrepo#downloads


Features
------------------------------------------------------------------------------
If you initiate your project with ``pygitrepo``, you are with these **powerful tools** out-of-the-box:


- ``make up``: single command to create / clean virtual environment. usually you do::
- ``make reformat``: command to Google stylize your code.
- ``make install``: (For end user) install your package (``setup.py`` file is out-of-the-box).
- ``make dev_install``: (For package developer) install your package in dev mode (``setup.py`` file is out-of-the-box).
- ``make test``: unittest with `pytest <https://pypi.python.org/pypi/pytest>`_ (tests folder and scripts is out-of-the-box, just follow the pattern and create more).
- ``make cov``: code coverage test with `coverage <https://pypi.python.org/pypi/coverage>`_, the default ``.coveragerc`` fit most of the case).
- ``make tox``: multi python version test with tox, the default ``tox.ini`` fit most of the case.
- built-in integration with https://travis-ci.org/.
- built-in integration with https://codecov.io/.
- ``make build_doc / view_doc``: easy sphinx document writing, no need to run ``sphinx-quickstart``, and write ``conf.py`` file.
- ``make deploy_doc``: deploy document to `AWS S3 <http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_.
- ``make publish``: publish your project to `PyPI <https://pypi.python.org/pypi>`_


``pygitrepo`` is compatible with Windows / MacOS / Linux, which means you can enjoy same patterns /
commands you use in development everywhere without and file changes.


Usage
------------------------------------------------------------------------------

**Command Line Tool**

1. Install: ``$ pip install pygitrepo``.
2. Run command line tool: ``$ pygitrepo-init``, entry your settings following the instruction.
3. A ``<repo-name>`` directory will be created, you can use this as your github repo directory.
4. Take a look at ``Makefile``, all magic happens here!


**Python Script Initializer**

If you want to programmatically initialize your repository, you can do:

.. code-block:: python

    import pygitrepo

    package_name = "obama_care" # import obama_care
    github_username = "Obama"
    supported_py_ver = ["2.7.13", "3.4.6", "3.5.3", "3.6.2"]
    author_name = "Obama"
    author_email = "example@email.com"
    license="MIT"
    s3_bucket = "doc-host"
    doc_service = "s3" # "none", "rtd", "s3"


    if __name__ == "__main__":
        pygitrepo.init(
            package_name=package_name,
            github_username=github_username,
            supported_py_ver=supported_py_ver,
            author_name=author_name,
            author_email=author_email,
            license=license,
            s3_bucket=s3_bucket,
            doc_service=doc_service,
        )

All available options and its definition can be found :meth:`~pygitrepo.cli.initiate_project`.


Software Environment You Should Have
------------------------------------------------------------------------------


For Windows (Git-Bash and MinGW)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Because Windows doesn't have ``shell script`` and ``make`` command, so we have to install some third-party software to make it works.

**Install Git Bash as shell emulator**

1. `Download and install git <https://git-scm.com/downloads>`_.
2. Now you can use ``C:\Program Files\Git\git-bash.exe`` compatible most of the command in MacOS/Linux.

**Install MinGW**

1. `Download and install <http://www.mingw.org/>`_, use the installer to install ``MinGW Base``.
2. Find ``C:\MinGW\bin\mingw32-make.exe``, copy and paste and rename as ``C:\MinGW\bin\make.exe``.
3. Add ``C:\MinGW\bin`` to $PATH (environment variable), so ``make`` command is available globally.

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
Use `AWS S3 <http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ to host your doc site is a good idea! its cheap, stable, and easy to deploy.

We need `awscli <https://aws.amazon.com/cli/>`_ to automate the deployment, and you need to create an `IAM user <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html>`_ and get API credential.

1. Install `awscli <https://aws.amazon.com/cli/>`_, just ``pip install awscli``.
2. `Configure your API token <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html>`_, just ``aws configure`` and follow the instruction.


Config PyPI (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to publish your package to `PyPI <https://pypi.python.org/pypi>`_ or `new PyPI <https://pypi.org/>`_, you need a pypi account and `Configure your credential <https://docs.python.org/2/distutils/packageindex.html#pypirc>`_.

1. Create a ``${HOME}/.pypirc`` file. ${HOME} is ``C:\Users\<username>`` in Windows and ``/Users/<username>`` in MacOS.
2. put these contents::

    [distutils]
    index-servers =
        pypi

    [pypi]
    username:<username>
    password:<password>

3. To publish your library, just ``make publish``.


CI (Continues Integration) (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. `Test with travis-ci <https://docs.travis-ci.com/user/languages/python/>`_, basically you just need to:
    - sign in using GitHub account.
    - toggle on your repo. just go to **https://travis-ci.org/<github_username>/<repo_name>?branch=master** and click **Activate**.
    - if it is the first time, you can manually start a first build.

2. `Code Coverage Test with codecov <https://github.com/codecov/example-python>`_.
    - sign in using GitHub account, that's it! it is automatically on if you have travis-ci.


.. _install:

Install
------------------------------------------------------------------------------

``pygitrepo`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install pygitrepo

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade pygitrepo