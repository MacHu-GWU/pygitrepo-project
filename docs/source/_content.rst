.. contents::

.. include:: ../../README.rst


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

1. Create a ``${HOME}/.pypirc`` file. ${HOME} is ``C:Users\<username>`` in Windows and ``/Users/<username>`` in MacOS.
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


.. _structure:

Project File Structure
------------------------------------------------------------------------------
A :green:`mature` python project should include these,

`File Structure Example <https://github.com/MacHu-GWU/pygitrepo-project>`_:

    |--- :ref:`repo_name`

        |--- :ref:`makes`

            |--- :ref:`python_env.mk`

        |--- :ref:`docs`

            |--- :ref:`sources`

                |--- :ref:`_static`

                    |--- :ref:`package_name-favicon.ico`

                    |--- :ref:`package_name-logo.png`

                |--- :ref:`_content.rst`

                |--- :ref:`author.rst`

                |--- :ref:`conf.py`

            |--- :ref:`Makefile <Makefile_doc>`

            |--- :ref:`create_doctree.py`

            |--- :ref:`make.bat`

        |--- :ref:`package_name`

            |--- :ref:`__init__.py`

        |--- :ref:`tests`

            |--- :ref:`all.py`

            |--- :ref:`test_import.py`

        |--- :ref:`.coveragerc`

        |--- :ref:`.gitattributes`

        |--- :ref:`.gitignore`

        |--- :ref:`.travis.yml`

        |--- :ref:`LICENSE.txt`

        |--- :ref:`MANIFEST.in`

        |--- :ref:`Makefile`

        |--- :ref:`README.rst`

        |--- :ref:`fixcode.py`

        |--- :ref:`release-history.rst`

        |--- :ref:`requirements.txt`

        |--- :ref:`requirements-dev.txt`

        |--- :ref:`requirements-doc.txt`

        |--- :ref:`requirements-test.txt`

        |--- :ref:`setup.py`

        |--- :ref:`tox.ini`


Dummy to Expert
------------------------------------------------------------------------------
If you are new in python development, you should know why awesome python project ``awesome``.


**Why Library?**

Writing bunch of scripts is NOT good. Because it will getting very big and unstructured very soon. To create an installable library for each python project takes these benefit:

1. smaller file, nice structure.
2. code is reusable accross the entire project.
3. easy to delivery.

But creating source distribution is really pain! (at lease for me for the first time). And there's a lots of tricky things for `setup.py file <https://docs.python.org/2/distutils/setupscript.html>`_. Sometime you don't know why it fails! ``pygitrepo`` helps you to create a nice, stable ``setup.py`` file.


**Continues Integration (CI) Test**

CI is basically ensure that your code is well tested at any point in your development time line.

It is important for open source project. Who can trust a project without test and 80% + code coverage?

`pytest <https://docs.pytest.org/en/latest/>`_ is the most powerful and semi standard test tool in Python Community. That's why ``pygitrepo`` use it.

`Travis-CI <https://travis-ci.org/>`_ provides free server and automatically test your code everytime you have new push to github. ``pygitrepo`` **creates the config file automatically** for `Travis-CI <https://docs.travis-ci.com/user/languages/python/>`_.

`Codecov <https://codecov.io/>`_ provides free server to display your code coverage status. ``pygitrepo`` also **creates the config file automatically** for that. And you can use ``make cov`` to test it.

You develop it on your favorite python version, but how do you know if it is compatible with other versions? `tox <https://tox.readthedocs.io/>`_ is the solution. ``pygitrepo`` **automatically generates the correct config file you need** (AGAIN). And you can use ``make tox`` to test against multiple python versions.


**Documentation does matter**

If yourself is the only user of your code, and you can live with only docstring and comments, you can skip this section. But if **there's other users and you want to advertise your project**, then documents matter.

`Sphinx Doc <http://www.sphinx-doc.org/>`_ is a semi standard doc builder in python community. ``pygitrepo`` will initialize the skeleton for you.


**Publish to PyPI**

Sharing is the soul of open source. And also your package is available via ``pip install xxx`` on cloud! Once you are confidence and finished the ``make test``, ``make cov``, ``make tox``, ``make build_doc``, ``make view_doc``, you are ready to do ``make publish``!.


**Congratulations, you are being more pro now!**


.. articles::

.. include:: author.rst


API Document
------------

* :ref:`by Name <genindex>`
* :ref:`by Structure <modindex>`
