# -*- coding: utf-8 -*-

"""
This is an example about how to read configs for your DevOps automation.

To read config values from file or external systems, first you need to
switch to a environment (dev / test / prod) using ``./config/switch-env dev``
in cli. Then import the ``config_init`` script that reads values from json
file and external systems.

To inject config values into other systems, you should dump the config to a
static json file ``config-final-for-python.json``, and allow other system to
read data from it.

.. code-block:: python

    config.CONFIG_DIR = join(dirname(dirname(__file__)), "config")
    config.dump_python_json_config_file()


config.dump_python_json_config_file()
"""

from os.path import dirname, join
from a_micro_service.devops.config_init import config

# read config values
print(config)

# inject config values to other system
config.CONFIG_DIR = join(dirname(dirname(__file__)), "config")
config.dump_serverless_json_config_file()
