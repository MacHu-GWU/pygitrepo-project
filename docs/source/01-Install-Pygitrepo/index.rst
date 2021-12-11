- :ref:`English <en_install_pygitrepo>`
- :ref:`中文 <cn_install_pygitrepo>`

.. _en_install_pygitrepo:

Install pygitrepo
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. Install ``pygitrepo`` Command Line Tool
------------------------------------------------------------------------------

``pygitrepo``itself is a Python library with a command line interface. Like the other similar python library ``pip``, ``pipenv``, ``virtualenv``. You can install it with ``pip``.

.. code-block:: bash

    # install and upgrade to latest
    $ pip install pygitrepo --upgrade

    # test with ``pgr`` command
    $ pgr


2. Update ``pygitrepo-config.json``
------------------------------------------------------------------------------

``pgr`` command requires a ``pygitrepo-config.json`` file at your git root directory. In other words, the ``pygitrepo-config.json`` file and ``.git`` hidden directory should be in the same directory. ``pygitrepo`` will check this to detect if the current directory is a valid ``pygitrepo`` compatible Python GitHub Repo. It allows you to use ``pgr`` command in any of it's sub directory.

The ``pygitrepo-config.json`` tells the ``pgr`` command which python version you want to use for local development, which service you want to use to host your document, etc...

If your repo skeleton is generated from https://github.com/MacHu-GWU/cookiecutter-pygitrepo, then you can just open ``pygitrepo-config.json`` and follow the instruction. An example can be found here https://github.com/MacHu-GWU/pygitrepo-project/blob/master/pygitrepo-config.json.
