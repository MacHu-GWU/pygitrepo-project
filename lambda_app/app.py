# -*- coding: utf-8 -*-

from chalice import Chalice

app = Chalice(app_name="pygitrep")


@app.lambda_function(name="hello-world")
def handler_hello_world(event, context):
    if event.get("name"):
        return "hello {}".format(event.get("name"))
    else:
        return "hello Mr X"
