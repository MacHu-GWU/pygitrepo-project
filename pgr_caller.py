# -*- coding: utf-8 -*-

import os
from pygitrepo.repo_config import RepoConfig

dir_here = os.path.dirname(os.path.abspath(__file__))

repo_config = RepoConfig()
print(repo_config.DIR_CWD.get_value())
print(repo_config.IS_PYGITREPO_DIR.get_value())

repo_config.read_pygitrepo_config_file()
print(repo_config.dir_project_root)
print(repo_config.DOC_HOST_AWS_PROFILE.get_value())