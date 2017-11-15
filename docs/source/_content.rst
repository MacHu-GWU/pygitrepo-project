.. contents::

.. include:: ../../README.rst

.. _structure:

Project File Structure
------------------------------------------------------------------------------
A mature python project should include these,

`File Structure Example <https://github.com/MacHu-GWU/pygitrepo-project>`_:

    |--- :ref:`repo_name`

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