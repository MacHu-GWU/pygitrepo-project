.. _use_pygitrepo:

Use pygitrepo
==============================================================================

There are two way of using ``pygitrepo``:

1. command line tool.
2. write a python script.

No matter what you are going to do, install ``pygitrepo`` first::

    $ pip install pygitrepo


Command Line Tool
------------------------------------------------------------------------------

Command line tool allows you to initiate a new project in current directory **with just with few types**.

Run command line tool: ``$ pygitrepo-init``, entry your settings following the instruction.

A ``<repo-name>`` directory will be created, you can use this as your github repo directory.
4. Take a look at ``Makefile``, all magic happens here!


Python Script
------------------------------------------------------------------------------

If you want to programmatically initialize your repository, you can do:

.. code-block:: python

    import pygitrepo

    package_name = "obama_care" # import obama_care
    github_username = "Obama"
    supported_py_ver = ["2.7.13", "3.4.6", "3.5.3", "3.6.2"]
    author_name = "Obama"
    author_email = "example@email.com"
    license="MIT"
    doc_host_bucket_name = "doc-host"
    doc_service = "s3" # "none", "rtd", "s3"

    if __name__ == "__main__":
        pygitrepo.init(
            package_name=package_name,
            github_username=github_username,
            supported_py_ver=supported_py_ver,
            author_name=author_name,
            author_email=author_email,
            license=license,
            doc_host_bucket_name=doc_host_bucket_name,
            doc_service=doc_service,
        )

All available options and its definition can be found `HERE <https://pygitrepo.readthedocs.io/pygitrepo/cli.html#pygitrepo.cli.initiate_project>`_ or `THERE <http://www.wbh-doc.com.s3.amazonaws.com/pygitrepo/cli.html#pygitrepo.cli.initiate_project>`_.


