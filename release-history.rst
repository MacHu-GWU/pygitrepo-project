.. _release_history:

Release and Version History
==============================================================================


1.0.4 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.3 (2021-12-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add AWS Chalice support, made AWS Lambda deployment easier.


1.0.2 (2021-12-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``pgr get-value ${attribute_name}`` subcommand, so you can pass value from python to shell scriptpgr


1.0.1 (2021-12-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- ``pygitrepo`` now it is a zero dependency cli tools. A simplified version of ``pipenv``


0.0.5 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Re-implement the interactive repo initialization script. Allows complex inter-option dependency logic which is not available in ``cookiecutter``
- If you are not using ``pyenv-virtualenv``, allows to activate virtualenv with ``source ./bin/py/activate.sh``.
- Add a powerful Centralized config management framework allows you to read and inject config values to any programming language, any system like AWS parameter store. And you can easily customize how's config been dynamically created.
- Add a Deployment on AWS best practice framework allows you to easily manage a multi-env dev/test/prod continues deployment workflow.
- Add CI/CD integration with CircleCI
- improve CI/CD integration with TravisCI

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.1 (2021-12-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- First release