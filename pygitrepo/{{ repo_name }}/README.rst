.. image:: https://travis-ci.org/{{ github_username }}/{{ repo_name }}.svg?branch=master
    :target: https://travis-ci.org/{{ github_username }}/{{ repo_name }}?branch=master

.. image:: https://codecov.io/gh/{{ github_username }}/{{ repo_name }}/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/{{ github_username }}/{{ repo_name }}

.. image:: https://img.shields.io/pypi/v/{{ package_name }}.svg
    :target: https://pypi.python.org/pypi/{{ package_name }}

.. image:: https://img.shields.io/pypi/l/{{ package_name }}.svg
    :target: https://pypi.python.org/pypi/{{ package_name }}

.. image:: https://img.shields.io/pypi/pyversions/{{ package_name }}.svg
    :target: https://pypi.python.org/pypi/{{ package_name }}

.. image:: https://img.shields.io/badge/Star_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/{{ github_username }}/{{ repo_name }}


Welcome to ``{{ package_name }}`` Documentation
==============================================================================

Documentation for ``{{ package_name }}``.


Quick Links
-----------

- .. image:: https://img.shields.io/badge/Link-Document-red.svg
      :target: http://{{ s3_bucket }}.s3.amazonaws.com/{{ package_name }}/index.html

- .. image:: https://img.shields.io/badge/Link-API_Reference_and_Source_Code-red.svg
      :target: API reference and source code <http://{{ s3_bucket }}.s3.amazonaws.com/{{ package_name }}/py-modindex.html

- .. image:: https://img.shields.io/badge/Link-Install-red.svg
      :target: `install`_

- .. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/{{ github_username }}/{{ repo_name }}

- .. image:: https://img.shields.io/badge/Link-Submit_Issue_and_Feature_Request-blue.svg
      :target: https://github.com/{{ github_username }}/{{ repo_name }}/issues

- .. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.python.org/pypi/{{ package_name }}#downloads


.. _install:

Install
-------

``{{ package_name }}`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install {{ package_name }}

To upgrade to latest version:

.. code-block:: console

	$ pip install --upgrade {{ package_name }}