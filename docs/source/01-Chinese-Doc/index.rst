Chinese Tutorial (中文文档点这里)
==============================================================================




pygitrepo 自带的文档插件
------------------------------------------------------------------------------

自定义字体颜色:

- This is :red:`Red`.
- This is :blue:`Blue`.

允许 jinja2 模板, 可排序表格:

.. jinja:: doc_data

    {{ doc_data.ltable_user.render() }}

拷贝代码到剪贴板:

.. code-block:: bash

    pip install pygitrepo --upgrade
