- :ref:`English <en_install_pygitrepo>`
- :ref:`中文 <cn_install_pygitrepo>`

.. _cn_install_pygitrepo:

安装 pygitrepo
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. 安装 ``pygitrepo`` 命令行工具
------------------------------------------------------------------------------

``pygitrepo`` 本身是一个 python 库, 只不过是一个自带命令行接口的库, 就和 ``pip``, ``pipenv``, ``virtualenv`` 类似. 所以你可以用 ``pip`` 命令安装.

.. code-block:: bash

    # 安装并升级到最新版本
    $ pip install pygitrepo --upgrade

    # 测试 ``pgr`` 命令
    $ pgr


2. 修改 ``pygitrepo-config.json``
------------------------------------------------------------------------------

``pgr`` 命令要求你的 git 工作目录的根目录下有一个 ``pygitrepo-config.json`` 文件, 也就是跟 ``.git`` 文件夹在同一个目录. 这决定了你当前所在的目录是否是一个 合法的, 和 ``pygitrepo`` 工具兼容的 Python Github Repo.

这个文件的主要作用是告知你想用哪个 Python 版本进行本地开发, 想用什么服务托管你的文档网站, 等等.

如果你的整个 Repo 的初始文件是用 https://github.com/MacHu-GWU/cookiecutter-pygitrepo 工具自动生成的, 那么你可以直接打开 ``pygitrepo-config.json`` 文件, 根据里面的注释的指引修改你的配置. 一个具体的例子可以参考 https://github.com/MacHu-GWU/pygitrepo-project/blob/master/pygitrepo-config.json.
