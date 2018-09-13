.. _professional_python:

Do Python Project in Professional Way
==============================================================================
If you are new in python development, you should know why awesome python project ``awesome``.



Why Creating a Python Library instead of bunch of scripts for your project?
------------------------------------------------------------------------------

Writing bunch of scripts is NOT good. Because code base will getting very big and unstructured shortly. And it is really difficult to reuse your code.

Creating an installable library for each python project takes these benefits:

1. smaller file, nice structure.
2. code is reusable across the entire project, or even for other project.
3. easy to delivery, publish, deploy.

However, **creating source distribution is really pain!** (at lease for me for the first time). And there's a lots of tricky things for `setup.py file <https://docs.python.org/2/distutils/setupscript.html>`_. Sometime you don't know why it fails! ``pygitrepo`` helps you to create a nice structured, highly customizable and stable ``setup.py`` file.


Continues Integration (CI) Test
------------------------------------------------------------------------------

`Continues Integration <https://www.thoughtworks.com/continuous-integration>`_ technique ensures that your code is well tested at any point in your development timeline.

Test is tmportant for open source project. Without endorsement by big commercial company, who can trust a project without test and 80% + code coverage?

`pytest <https://docs.pytest.org/en/latest/>`_ is the most powerful and semi standard test tool in Python Community. That's why ``pygitrepo`` use it.

`Travis-CI <https://travis-ci.org/>`_ provides free server and automatically test your code everytime you have new push to github. ``pygitrepo`` **creates the config file automatically** for `Travis-CI <https://docs.travis-ci.com/user/languages/python/>`_.

`Codecov <https://codecov.io/>`_ provides free server to display your code coverage status. ``pygitrepo`` also **creates the config file automatically** for that. And you can use ``make cov`` to test it.

You develop it on your favorite python version, but how do you know if it is compatible with other versions? `tox <https://tox.readthedocs.io/>`_ is the solution. ``pygitrepo`` **automatically generates the correct config file you need** (AGAIN). And you can use ``make tox`` to test against multiple python versions.


Documentation does matter
------------------------------------------------------------------------------

If yourself is the only user of your code, and you can live with only docstring and comments, you can skip this section. But if **there's other users and you want to advertise your project**, then documents matter.

`Sphinx Doc <http://www.sphinx-doc.org/>`_ is a semi standard doc builder in python community. ``pygitrepo`` will initialize the skeleton for you.


Publish to PyPI
------------------------------------------------------------------------------

Sharing is the soul of open source. And also your package is available via ``pip install xxx`` on cloud! Once you are confidence and finished the ``make test``, ``make cov``, ``make tox``, ``make build_doc``, ``make view_doc``, you are ready to do ``make publish``!.


**Congratulations, you are being more pro now!**
