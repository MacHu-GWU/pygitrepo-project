# -*- coding: utf-8 -*-

import os
import pytest
from pygitrepo.repo_config import RepoConfig

dir_here = os.path.dirname(os.path.abspath(__file__))
dir_project_root = os.path.dirname(dir_here)


class TestRepoConfig(object):
    def test(self):
        cwd = os.getcwd()
        os.chdir(dir_project_root)
        config = RepoConfig()
        config.read_pygitrepo_config_file()
        os.chdir(cwd)

        for k, v in RepoConfig.__dict__.items():
            if isinstance(v, property):
                getattr(config, k)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
