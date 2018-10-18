# -*- coding: utf-8 -*-

from rstobj.directives import ListTable

ltable_user = ListTable(
    data=[["id", "name"], [1, "Alice"], [2, "Bob"], [3, "Cathy"]],
    title="User",
    index=False,
    header=True,
    class_="sortable",
)

doc_data = dict(
    ltable_user=ltable_user,
    topic="This is a Topic",
)
