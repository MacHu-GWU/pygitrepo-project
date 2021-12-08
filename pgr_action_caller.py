# -*- coding: utf-8 -*-


from pygitrepo.repo_config import RepoConfig
from pygitrepo.actions import actions

repo_config = RepoConfig()
repo_config.read_pygitrepo_config_file()

# actions.venv_up(repo_config)
# actions.venv_remove(repo_config)
# actions.pip_dev_install(repo_config)
# actions.pip_install(repo_config)
# actions.pip_uninstall(repo_config)
# actions.req_dev(repo_config)
# actions.req_doc(repo_config)
# actions.req_test(repo_config)
# actions.req_info(repo_config)
# actions.test_pytest_only(repo_config)
# actions.test_pytest(repo_config)
# actions.test_cov_only(repo_config)
# actions.test_cov(repo_config)
# actions.test_tox_only(repo_config)
# actions.test_tox(repo_config)
# actions.reformat_pep8_code_style(repo_config)
# actions.build_doc_only(repo_config)
# actions.build_doc(repo_config)
# actions.view_doc(repo_config)
# actions.deploy_doc_to_versioned(repo_config)
# actions.deploy_doc_to_latest(repo_config)
# actions.deploy_doc(repo_config)
# actions.publish_to_pypi(repo_config)
# actions.run_jupyter_notebook(repo_config)
# actions.build_lambda_source_code(repo_config)
# actions.upload_lambda_source_code(repo_config)
# actions.build_lambda_layer(repo_config)
# actions.upload_lambda_layer(repo_config)
# actions.deploy_lambda_layer(repo_config)