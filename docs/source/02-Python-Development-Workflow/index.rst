- :ref:`English <en_python_development_workflow>`
- :ref:`中文 <cn_python_development_workflow>`

.. _cn_python_development_workflow:

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

**关于发布文档**

1. **文档网站的本质**: 首先需要知道的是, sphinx doc 构建的文档本质上是一对 html css 文件, 网站也是一个静态的网站 (静态的意思是没有注册之类的需要跟服务器互动的功能, 只有简单的站内搜索功能). 市面上有非常多的工具可供托管静态网站.
2. **Readthedocs 文档托管服务**: https://readthedocs.org/ 是 Python 社区最流行的文档托管服务提供商, 可提供开源项目的文档托管, 以及自动化构建. 其原理是当你把代码 push 到 GitHub (或是其他 Git 托管网站) 后, 自动拉取最新的代码, 并用 sphinx doc 进行文档构建, 成功后即将其发布到 ``https://${project_name}.readthedocs.org``.
3. **用 AWS S3 托管静态网站**: AWS (Amazon Web Service) 作为世界第一的公共云服务提供商, 它的 `AWS S3 提供了廉价的静态网站托管服务 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html>`_. 并且能够配置访问权限, 允许特定的 IP 区间访问网站. 该方案适合私有 Python 库的私有文档, 只允许公司内网和授权的人访问文档. 该方案 安全, 廉价, 方便.

**关于文档版本**

作为开源软件, 你的 Python 包是有版本的. 同样的你的文档也应该有版本. Readthedocs 提供了一个选项可以启用版本, 最新版本的文档永远是 ``https://${project_name}.readthedocs.org/latest``, 版本号专用文档则是 ``https://${project_name}.readthedocs.org/${version}``. 如果你用 AWS S3 托管服务, 那么你同样可以将文档部署到不同的目录下以区分版本.

**将当前版本的文档作为版本专用文档部署到 AWS S3**

.. code-block:: bash

    pgr deploy-doc-to-versioned

**将当前版本的文档作为最新文档部署到 AWS S3**

.. code-block:: bash

    pgr deploy-doc-to-latest

**将当前版本的文档同时作为版本专用和最新文档部署到 AWS S3**

.. code-block:: bash

    pgr deploy-doc


7. 发布到 PyPI
------------------------------------------------------------------------------

**将当前版本发布到 PyPI**

.. code-block:: bash

    pgr publish

作为一个 Python 库, 最大的荣耀是发布到 PyPI 被很多人下载使用, 给他人带来价值. `PyPI <https://pypi.org/>`_ 是 Python 软件基金会提供的开源 Python 库托管服务. 大家平时用的 Python 库也是从这里下载来的. 为了将你的包发布到 PyPI, 你需要 ``wheel`` 和 ``twine`` 这两个官方推荐的工具, 将你的源码打包, 加上元信息, 然后发布到 PyPI.


总结
------------------------------------------------------------------------------

至此, 一个完整的 Python 库的开发工作流就介绍完了.
