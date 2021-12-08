# -*- coding: utf-8 -*-

import os
import sys
import pytest

dir_here = os.path.dirname(os.path.abspath(__file__))
dir_project_root = os.path.dirname(dir_here)
if dir_project_root not in sys.path:
    sys.path.append(dir_project_root)

from pygitrepo.repo_config import RepoConfig
from pygitrepo.actions import actions


class TestActions(object):
    def test(self):
        cwd = os.getcwd()
        os.chdir(dir_project_root)
        config = RepoConfig()
        config.read_pygitrepo_config_file()

        # before the pytest testing, it will load entire python library
        # to memory. In other word, if it is already in memory, you can safely
        # remove virtual environment.
        #
        # in order to recovery the virtualenv again, we have to run
        # venv_up, pip_dev_install, req_test to recover it back to the correct state
        actions.venv_remove(config)
        actions.venv_up(config)
        actions.pip_dev_install(config)
        actions.req_test(config)
        actions.req_dev(config)
        actions.req_doc(config)
        actions.req_info(config)

        # actions.build_doc(config)
        actions.info(config)
        actions.build_lambda_source_code(config)


        # caution! don't clean up tox dir, if you are testing this in
        # tox environment, it will disturb other py version testing.
        actions.clean_doc(config)
        # actions.clean(config, ignore_tox=True)

        # if "CI" not in os.environ:
        #     actions.upload_lambda_source_code(config)

        if ("TOX_WORK_DIR" not in os.environ) and ("CI" not in os.environ):
            actions.upload_lambda_source_code(config)
            actions.build_upload_deploy_lambda_layer(config)

        os.chdir(cwd)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
