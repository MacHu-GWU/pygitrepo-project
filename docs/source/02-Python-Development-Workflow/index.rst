- :ref:`English <en_python_development_workflow>`
- :ref:`中文 <cn_python_development_workflow>`

.. _en_python_development_workflow:

Python Development Workflow
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is Python Development Workflow
------------------------------------------------------------------------------

There are a lots of common process in a Python project development life cycle, for instances:

1. create / remove dev virtual environment
2. install dependencies
3. unit test, code coverage test, matrix test
4. build document, preview document
5. build and publish to PyPI.

These common processes natively are just combination of CLI command. You may need to resolve some directory or file path issue, and run different commands conditionally. ``pygitrepo`` simplified those process, and provide a consistent development experience for all developer.


1. Display useful information
------------------------------------------------------------------------------

Display important information you need to know in this workflow.

.. code-block:: bash

    pgr info


2. Create / Remove virtual environment
------------------------------------------------------------------------------

**Create virtual environment**. It locate at ``${HOME}/venvs/python/${PYTHON_VERSION}/${PROJECT_NAME}_venv``, example ``${HOME}/venvs/python/3.8.11/pygitrepo_venv``. We try to isolate the venv dir from GitHub repository dir, avoid committing to the git. :meth:`~pygitrepo.repo_config.RepoConfig.dir_venv`.

.. code-block:: bash

    pgr venv-up

**Remove virtual environment**. Remove the venv folder.

.. code-block:: bash

    pgr venv-remove


3. Install Dependencies
------------------------------------------------------------------------------

**Install dependencies and the python package you are developing itself to virtual environment**, if force to uninstall existing python package, make sure it meets the definition in ``requirements.txt`` file.

.. code-block:: bash

    pgr pip-dev-install

**Remove the python package you are developing from virtual environment, keep other dependencies**

.. code-block:: bash

    pgr pip-uninstall

**Pip Install requirements-dev.txt**

.. code-block:: bash

    pgr req-dev

**Pip Install requirements-doc.txt**

.. code-block:: bash

    pgr req-doc

**Pip Install requirements-test.txt**

.. code-block:: bash

    pgr req-test


4. Run Test
------------------------------------------------------------------------------

**Run all unit test with pytest, don't reuse any cache**

.. code-block:: bash

    pgr test # another version is ``pgr test-only``, it reuse cache.

**Run code coverage test with pytest-cov, don't reuse any cache**

.. code-block:: bash

    pgr cov # another version is ``pgr cov-only``, it reuse cache.

**Run matrix test with tox, don't reuse any cache**

.. code-block:: bash

    pgr tox # another version is ``pgr tox-only``, it reuse cache.


5. Normalize your Python Code Style
------------------------------------------------------------------------------

**Normalize your Python Code Style in your python source code dir and tests dir**

.. code-block:: bash

    pgr pep8

- `pep8 <https://www.python.org/dev/peps/pep-0008/>`_
- `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`_
- `Black <https://black.readthedocs.io/en/stable/>`_


6. Build and Publish Documents
------------------------------------------------------------------------------

**Build docs on local with sphinx-doc**

.. code-block:: bash

    pgr build-doc # another version is ``pgr build-doc-only``, it reuse cache.

**Preview recently built local documents**

.. code-block:: bash

    pgr view-doc

**Remove recently built doc**

.. code-block:: bash

    pgr clean-doc

**Deploy recently built docs as versioned doc to AWS S3**

.. code-block:: bash

    pgr deploy-doc-to-versioned

**Deploy recently built docs as latest doc to AWS S3**

.. code-block:: bash

    pgr deploy-doc-to-latest

**Deploy recently built docs as versioned doc and also latest doc to AWS S3**

.. code-block:: bash

    pgr deploy-doc


7. Publish to PyPI
------------------------------------------------------------------------------

**Publish current version to PyPI**

.. code-block:: bash

    pgr publish


Summary
------------------------------------------------------------------------------

All Done.
