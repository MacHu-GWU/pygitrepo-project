.. image:: https://readthedocs.org/projects/pygitrepo/badge/?version=latest
    :target: https://pygitrepo.readthedocs.io/?badge=latest
    :alt: Documentation Status

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

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/pygitrepo-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: https://pygitrepo.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: https://pygitrepo.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
      :target: https://pygitrepo.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
      :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/pygitrepo-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: https://github.com/MacHu-GWU/pygitrepo-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: https://github.com/MacHu-GWU/pygitrepo-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.org/pypi/pygitrepo#files


Welcome to ``pygitrepo`` Documentation
==============================================================================

``pygitrepo`` is a tool that can initiate a professional-liked python project skeleton from scratch, **JUST NEED TO ENTER THE LIBRARY NAME!**

**WITHOUT** ``pygitrepo``:

.. code-block:: bash

    $ git init my_library # initiate your git repo
    $ vim .gitignore # edit .gitignore file

    $ virtualenv my_library_venv # create venv
    $ source ./my_project_venv/bin/activate # activate venv
    $ vim setup.py # edit setup.py file, DO YOU REALLY KNOW HOW TO WRITE setup.py FILE?
    $ pip install . # install your library and dependencies
    $ pip install pytest
    $ mkdir tests # write some test
    $ pip install sphinx
    $ sphinx-quickstart # initiate doc
    $ vim docs/source/conf.py # configure your doc settings

Now you finally read to start **writing the real code**. However, it could be more complicate on Windows.

After you finished your development, you want to test it before you publish:

.. code-block:: bash

    $ vim .travis.yml # configure your continues-integration, or use .circleci
    $ vim tox.ini # configure tox to test on Py2.7, 3.4, 3.5, ...
    $ vim .coveragerc # configure code coverage test
    $ pip install tox
    $ pip install coverage

I guess it would **take you at least AN HOUR to read the document for continues integration, code coverage test, and multiple python version test**... Do you know how many pitfalls are in these?

**But if WITH** ``pygitrepo``:

.. code-block:: bash

    $ pip install pygitrepo
    $ pygitrepo-init # call the command line tool, and enter your project name
    (REQUIRED) Your Package Name (e.g. pip): pygitrepo
    (REQUIRED) Your Github Username: Machu-GWU
    more optional prompt, you can use the default ...

**Done!**

a new git repo directory ``my_library-project`` will be created. ``.gitignore``, ``setup.py``, ``requirements-dev/doc/test.txt``, ``.travis.yml``, ``.coveragerc``, ``docs/source/conf.py``, ``tests/some_test.py ...``, etc, ... All functions are ready to use, you don't need to edit anything!

Create and Remove virtualenv:

.. code-block:: bash

    $ make up # create
    $ make clean # remove

Install your library and Run Test:

.. code-block:: bash

    $ make test # unit test
    $ make cov # code coverage test
    $ make tox # multi python version test

Build Document with auto-generated API reference:

.. code-block:: bash

    $ make build_doc # build your document site
    $ make view_doc # open your doc in browser
    $ make deploy_doc # deploy your doc website to s3

Want to publish to Python Package Index?, Let's do:

.. code-block:: bash

    $ make publish


.. _install:

Install
------------------------------------------------------------------------------

``pygitrepo`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install pygitrepo

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade pygitrepo