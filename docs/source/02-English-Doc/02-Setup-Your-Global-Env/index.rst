.. _setup_your_global_env:

Setup your global environment before using pygitrepo
==============================================================================

Before you start doing real development in Python, you need some setup for your system environment. I know, it is painful. But don't worry, we **only do it once in our life time**.


Windows does NOT have bash shell
------------------------------------------------------------------------------

90% of servers, include build, test, deployment server are running on Linux based system. It is better to do the development on same platform as the production environment. **Most of Linux command works on MacOS**, so there is no problem if you have a Mac.

But if you use **Windows**, the command line syntax and interface in Windows is different from MacOS and Linux. You should install ``git-bash`` as an alternative of bash in Linux, which is a part of the `git <https://git-scm.com/downloads>`_.


Install Git Bash for Windows
------------------------------------------------------------------------------

1. `Download and install git <https://git-scm.com/downloads>`_.
2. Now you can use ``C:\Program Files\Git\git-bash.exe`` as your default terminal. It is compatible with most of the commands in MacOS/Linux.


Windows does NOT have make command
------------------------------------------------------------------------------

The purpose of the make utility is to determine automatically which pieces of a large program need to be recompiled, and issue the commands to recompile them. make with any programming language whose compiler can be run with a shell command.

In python project, Makefile can be used to issue group of shell commands.


Install MinGW for Windows
------------------------------------------------------------------------------

1. `Download and install <http://www.mingw.org/>`_, use the installer to install ``MinGW Base``.
2. Find ``C:\MinGW\bin\mingw32-make.exe``, copy and paste and rename as ``C:\MinGW\bin\make.exe``.
3. Add ``C:\MinGW\bin`` to $PATH (environment variable), so ``make`` command is available globally.

Now you can use ``make <target>`` in ``git-bash.exe`` now.


MacOS does NOT have Package Manager
------------------------------------------------------------------------------

Linux has its own built-in package manager command line tool, such as ``yum`` for RedHat, ``apt`` for Debian and Ubuntu. Mac doesn't come with one by default.

`HomeBrew <https://brew.sh/>`_ is the most popular alternative package manager for Mac. It is a must-have tools for developer.


Install HomeBrew for MacOS
------------------------------------------------------------------------------

Got `HomeBrew Homepage <https://brew.sh/>`_, the installation is just one line of command!

Then, test if ``brew`` command works.


Install your main Python interpreter
------------------------------------------------------------------------------

**Windows**

You can find the executable install for all Python versions here: https://www.python.org/downloads/windows/.

For multiple python version, just install multiple python, and rename the ``python.exe`` to ``python{major_version}{minor_version}.exe`` respectively, for example, ``python27.exe``, ``python34.exe``, ``python35.exe``, ``python36.exe``, ...

Add add those path to your $PATH environmental varible.

Don't forget to test if those commands works: ``python27``, ``python34``, ...


**MacOS**

MacOS comes with Python27 by default, and it is supporting a lots of system service. I HIGHLY RECOMMEND that DO NOT MESS UP WITH YOUR SYSTEM PYTHON ENVIRONMENT. Use `pyenv <https://github.com/pyenv/pyenv>`_ to install any python version you want on your mac.

Install pyenv::

    $ brew install pyenv

Install Python from pyenv::

    $ pyenv install 2.7.13

List all available Python versions in pyenv::

    $ pyenv install -l


**Linux**

Linux comes with Python by default, and it is supporting a lots of system service. I HIGHLY RECOMMEND that DO NOT MESS UP WITH YOUR SYSTEM PYTHON ENVIRONMENT. If you need Python3.X, please read this article `Installing Python 3 on Linux <https://docs.python-guide.org/starting/install3/linux/>`_.


Install ``pip`` and ``virtualenv``
------------------------------------------------------------------------------

`pip <https://pip.pypa.io/en/stable/installing/>`_ is the python package manager tool. And `virtualenv <https://virtualenv.pypa.io/en/stable/>`_ can separate your development python environment from your system python environment. These are the two must-have tool for Python.

If you have multiple python version, you only need to install ``virtualenv`` in your main python version. It will automatically been installed when creating a virtual environment.


Use ``pyenv-virtualenv`` in MacOS (Optional)
------------------------------------------------------------------------------

There are two ways of using ``virtualenv`` in MacOS:

1. Use generic `virtualenv <https://virtualenv.pypa.io/en/stable/>`_.
2. Use `pyenv <https://github.com/pyenv/pyenv>`_ + `pyenv-virtualenv <https://github.com/pyenv/pyenv-virtualenv>`_.

I prefer ``pyenv`` + ``pyenv-virtualenv``, because it allows you:

1. use tox to test against multiple python version locally before using cloud CI (continues integration).
2. will not mess up your global python environment.
3. the ``Makefile`` will do the ``pyenv`` + ``pyenv-virtualenv`` setup for you, just make sure that you have  `HomeBrew <https://brew.sh/>`_ installed.

.. note::

    ``pygitrepo`` use ``pyenv`` + ``pyenv-virtualenv`` on MacOS by default


AWS Command Line (Optional)
------------------------------------------------------------------------------

The most popular method of hosting your documentation is `ReadTheDoc hosting service <https://readthedocs.org/>`_. It is free for open source project.

Using `AWS S3 <http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ **to host your doc site is another great idea! It's cheap, stable, and easy to deploy, and you have full privacy control of it**.

We need `awscli <https://aws.amazon.com/cli/>`_ to automate the deployment, and you need to create an `IAM user <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html>`_ and get the API credential.

1. Install `awscli <https://aws.amazon.com/cli/>`_, just ``pip install awscli``.
2. `Configure your API token <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html>`_, just ``aws configure`` and follow the instruction.

Then test with ``aws s3 ls`` to see if your AWS command line works.


Config PyPI (Optional)
------------------------------------------------------------------------------

Python is an open source project. Why not publish your package to `PyPI <https://pypi.org/>`_, share your awesome code with developers all over the world?

To get started, you need a `PyPI Account <https://pypi.org/account/register/>`_ account and `configure your credential <https://docs.python.org/3/distutils/packageindex.html#pypirc>`_. for your computer.

1. Create a ``${HOME}/.pypirc`` file. ${HOME} is ``C:Users\<username>`` in Windows, ``/Users/<username>`` in MacOS, ``/home/<username>`` in Linux.
2. put these contents::

    [distutils]
    index-servers =
        pypi

    [pypi]
    username:<username>
    password:<password>

3. To publish your library, just ``make publish``.


CI (Continues Integration) (Optional)
------------------------------------------------------------------------------

Full test your code automatically every time you commit to git can guard your project from most of the ridiculous bug. `Continues Integration <https://www.thoughtworks.com/continuous-integration>`_ is the tool for this.

1. `Test with travis-ci <https://docs.travis-ci.com/user/languages/python/>`_, basically you just need to:
    - sign in using GitHub account.
    - toggle on your repo. just go to **https://travis-ci.org/<github_username>/<repo_name>?branch=master** and click **Activate**.
    - if it is the first time, you can manually trigger a first build (More options -> Trigger a custom build.

2. `Code Coverage Test with codecov <https://github.com/codecov/example-python>`_.
    - sign in using GitHub account, that's it! Everything is automatically done if you have travis-ci.
