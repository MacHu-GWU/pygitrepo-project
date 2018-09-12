{%- if doc_service == "rtd" %}
.. image:: https://readthedocs.org/projects/{{ rtd_name }}/badge/?version=latest
    :target: https://{{ rtd_name }}.readthedocs.io/?badge=latest
    :alt: Documentation Status
{% endif %}
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

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: {{ repo_url }}

------

{% if doc_domain %}
.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: {{ doc_domain }}/index.html
{% endif %}

{%- if doc_domain %}
.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: {{ doc_domain }}/py-modindex.html
{% endif %}

{%- if doc_domain %}
.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
      :target: {{ doc_domain }}/py-modindex.html
{% endif %}
.. image:: https://img.shields.io/badge/Link-Install-blue.svg
      :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: {{ repo_url }}

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: {{ repo_url }}/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: {{ repo_url }}/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.org/pypi/{{ package_name }}#files


Welcome to ``{{ package_name }}`` Documentation
==============================================================================

Documentation for ``{{ package_name }}``.


.. _install:

Install
------------------------------------------------------------------------------

``{{ package_name }}`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install {{ package_name }}

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade {{ package_name }}