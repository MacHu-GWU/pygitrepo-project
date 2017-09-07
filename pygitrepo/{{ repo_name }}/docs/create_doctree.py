#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docfly
from pathlib_mate import Path
import {{package_name}} as package

source_dir = Path(__file__).absolute().parent.append_parts("source").abspath

# --- Manually Made Doc ---
# Comment this if you don't follow this style guide.
# http://www.wbh-doc.com.s3.amazonaws.com/docfly/02-sphinx-doc-style-guide/index.html
doc = docfly.DocTree(source_dir)
doc.fly(table_of_content_header="Table of Content")

# --- Api Reference Doc ---
package_name = package.__name__
doc = docfly.ApiReferenceDoc(
    package_name,
    dst=source_dir,
    ignored_package=[
        "%s.pkg" % package_name,
        "%s.zzz_ezinstall.py" % package_name,
    ]
)
doc.fly()
