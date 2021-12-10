- :ref:`English <en_python_development_workflow>`
- :ref:`中文 <cn_python_development_workflow>`

.. _cn_python_development_workflow:

Python 开发工作流
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


什么是开发工作流
------------------------------------------------------------------------------

在 Python 库的开发过程中, 有许多步骤是通用的, 例如:

1. 创建 / 删除 虚拟环境
2. 安装依赖
3. 单元测试, 代码覆盖率测试, 矩阵测试
4. 构建文档, 查看文档
5. 打包发布

这些步骤对于大部分的 Python 项目都是通用的, 每个步骤通常都由多个命令行命令排列组合而成, 其中要解决一些文件路径的问题, 以及文件系统的情况的条件判断. 而 ``pygitrepo`` 工具将这些复杂的步骤自动化了, 使得一个项目中的所有人在不同的机器上有着一致的开发体验.


1. 显示有用的信息
------------------------------------------------------------------------------

整个工作流会用到的重要信息.

.. code-block:: bash

    pgr info


2. 创建 / 删除 虚拟环境
------------------------------------------------------------------------------

**创建虚拟环境**. 具体的路径在 ``${HOME}/venvs/python/${PYTHON_VERSION}/${PROJECT_NAME}_venv``, example ``${HOME}/venvs/python/3.8.11/pygitrepo_venv``. 该路径和 GitHub repository 分离, 以避免将虚拟环境 commit 到 git 中. :meth:`~pygitrepo.repo_config.RepoConfig.dir_venv`.

.. code-block:: bash

    pgr venv-up

**删除虚拟环境**. 即删除整个虚拟环境文件夹.

.. code-block:: bash

    pgr venv-remove


3. 安装包依赖
------------------------------------------------------------------------------

**安装库本身及其包依赖到虚拟环境**, 会先强制删除已有的安装, 确保执行命令后的包是最新状态.

.. code-block:: bash

    pgr pip-dev-install

注:

    ``包``, ``库`` 都是同样的概念, 都是可安装的 Python package, 也就是你 ``pip install ${name}`` 中 ``${name}`` 对应的部分.

在 ``pygitrepo`` 的最佳实践中, 我们将依赖的第三方包分门别类放在不同的文件中.

- ``requirements.txt``: 开发你的 Python 库所需要的必要的包. 请尽量精简.
- ``requirements-dev.txt``: 在开发过程中能提高你开发效率或是任何能帮助你开发的包. 例如 debug 用的 `icecrean <https://pypi.org/project/icecream/>`_, `rich <https://pypi.org/project/rich/>`_, 打包发布所用的 `twine <https://pypi.org/project/twine/>`_.
- ``requirements-test.txt``: 测试时用到的包. 例如单元测试框架 `pytest <https://pypi.org/project/pytest/>`_, 测试覆盖率框架 `pytest-cov <https://pypi.org/project/pytest-cov/>`_.
- ``requirements-doc.txt``: 在构建你的项目文档时用到的包. 例如 `sphinx-doc <https://pypi.org/project/Sphinx/>`_.

我们自己要开发的 Python 库本身里面的各个模块, 可能要互相 import. 在 unittest 中你也需要 import 自己的库. 所以我们需要将正在开发的库本身也安装到虚拟环境中. 这里我们要用 ``pip install -e`` 选项. `-e <https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-e>`_ 是 editable (可编辑) 的意思, 意思是你对当前 Github Repo 中的库的源码做的任何修改都会直接在你的虚拟环境中生效. 本质上 Python 是创建了一个 egg link, 连接到你的 Repo 根目录下的源码.

**从虚拟环境中删除当前包本身, 不删除依赖**

.. code-block:: bash

    pgr pip-uninstall

**安装 requirements-dev.txt 中的依赖**

.. code-block:: bash

    pgr req-dev

**安装 requirements-doc.txt 中的依赖**

.. code-block:: bash

    pgr req-doc

**安装 requirements-test.txt 中的依赖**

.. code-block:: bash

    pgr req-test


4. 执行测试
------------------------------------------------------------------------------

**用 pytest 执行全部单元测试, 不使用任何缓存**

.. code-block:: bash

    pgr test # 还有一个版本是 pgr test-only, 区别是使用缓存.

**用 pytest + coverage** 执行代码覆盖率测试, 不使用任何缓存**

.. code-block:: bash

    pgr cov # 还有一个版本是 pgr cov-only, 区别是使用缓存.

**用 pytest + tox** 执行矩阵测试, 不使用任何缓存**

.. code-block:: bash

    pgr tox # 还有一个版本是 pgr tox-only, 区别是使用缓存.

这里做一下解释.

1. pytest 是 python 社区事实上的单元测试框架标准, 虽然有很多其他选择, 大部分有影响力的 python 开源项目都选择了 pytest, 并且 pytest 的插件生态最为丰富, 更新最为频繁.
2. **代码覆盖率测试** 的目的是确保你的测试用例会使用到代码库中所有的代码. 并且自动生成报告, 告诉你每个 .py 文件以及整个项目的覆盖百分比, 以及具体哪一个文件哪一行没有被覆盖到. 一般工业中测试覆盖率不到 95% 不敢在生产环境中使用, 不到 90% 不能称之为稳定.
3. **矩阵测试** 主要是一种被要发布到社区供很多人使用的测试方式. 因为用户使用的操作系统各种各样, 使用的 Python 版本也是各不相同, 作为开源软件需要确保能在各种操作系统以及各种 Python 版本上都能正常工作. `tox <https://tox.wiki/en/latest/>`_ 是 Python 社区矩阵测试的事实标准.


5. 标准化你的代码风格
------------------------------------------------------------------------------

**标准化你的源码文件夹以及测试文件夹下所有 Python 文件的代码风格**

.. code-block:: bash

    pgr pep8

Python 社区的代码风格有很多种. 官方推荐的风格叫 pep8, 属于早期制定的标准. Google Python Style Guide 也很有名, 在网络上被转载的次数最多. 而 Black 则是比较新的标准, 要求非常严格, 不给你做选择的余地, 但是被大量优秀的开源库所使用. ``pygitrepo`` 中目前只支持自动 ``pep8``. 在团队合作中, 用工具自动标准化代码风格有助于简化 code review 的流程, 避免争端.

- `pep8 <https://www.python.org/dev/peps/pep-0008/>`_
- `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`_
- `Black <https://black.readthedocs.io/en/stable/>`_


6. 构建和发布文档
------------------------------------------------------------------------------

**在本地用 sphinx-doc 构建文档**

.. code-block:: bash

    pgr build-doc # 还有一个版本是 pgr build-doc-only, 区别是使用缓存.

**预览刚刚在本地构建的文档**

.. code-block:: bash

    pgr view-doc

**删除刚刚在本地构建的文档**

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
