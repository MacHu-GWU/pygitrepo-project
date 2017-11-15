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
- continues integration for **unit test and code coverage on your local machine and also cloud**.
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

- ``make up``: single command to create / clean virtual environment.
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

``pygitrepo`` is compatible with Windows / MacOS / Linux, which means you can enjoy same patterns / commands you use in development everywhere without and file changes.


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

All available options and its definition can be found `HERE <https://pygitrepo.readthedocs.io/pygitrepo/cli.html#pygitrepo.cli.initiate_project>`_ or `THERE <http://www.wbh-doc.com.s3.amazonaws.com/pygitrepo/cli.html#pygitrepo.cli.initiate_project>`_.


.. _install:

Install
------------------------------------------------------------------------------

``pygitrepo`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install pygitrepo

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade pygitrepo