# -*- coding: utf-8 -*-

import os
import sys
import json
from .pkg.configirl import ConfigClass, Constant, Derivable
from . import constants
from .helpers import (
    join_s3_uri,
    split_s3_uri,
    s3_key_smart_join,
    make_s3_console_url,
    s3_uri_to_url,
    strip_comments,
)
from .operation_system import (
    OS_NAME, IS_WINDOWS, IS_MACOS, IS_LINUX, IS_JAVA, OPEN_COMMAND
)


class _BaseConfig(ConfigClass):
    def ensure_attr_not_none(self, attr_name):
        value = getattr(self, attr_name).get_value()
        if value is None:
            raise ValueError(
                "Please give '{}' a valid value other than 'None'!".format(
                    attr_name
                )
            )


class _RepoConfig(_BaseConfig):
    PACKAGE_NAME = Constant(default=None)
    GITHUB_ACCOUNT = Constant(default=None)
    GITHUB_REPO_NAME = Constant(default=None)

    # The main python version you use for development
    DEV_PY_VER_MAJOR = Constant(default=None)
    DEV_PY_VER_MINOR = Constant(default=None)
    DEV_PY_VER_MICRO = Constant(default=None)

    TOX_TEST_VERSIONS = Constant(default=lambda: list())

    @property
    def package_name_slugify(self):
        return self.PACKAGE_NAME.get_value().replace("_", "-")


class _DocConfig(_BaseConfig):
    """
    Documentation build related config.
    """
    DOC_HOST_RTD_PROJECT_NAME = Constant(default=None)
    """
    If you choose to host your document on https://readthedocs.org/, it is  
    the project name for https://readthedocs.org/, your documentation website
    url will become https://${DOC_HOST_RTD_PROJECT_NAME}.readthedocs.io/
    """

    DOC_HOST_AWS_PROFILE = Constant(default=None)
    """
    If you choose to host your document on AWS S3 as static site, it is the 
    AWS named profile you use to authenticate for uploading doc files to AWS S3 
    """

    DOC_HOST_S3_BUCKET = Constant(default=None)
    """
    If you choose to host your document on AWS S3 as static site, it is the 
    bucket you use to host this project.
    """


class _AWSLambdaConfig(_BaseConfig):
    AWS_LAMBDA_DEPLOY_AWS_PROFILE = Constant(default=None)
    """
    The AWS named profile you use to authenticate for AWS Lambda deployment.
    """

    AWS_LAMBDA_DEPLOY_S3_BUCKET = Constant(default=None)
    """
    The AWS S3 bucket for Lambda deployment
    """

    AWS_LAMBDA_BUILD_DOCKER_IMAGE = Constant(default=None)
    AWS_LAMBDA_BUILD_DOCKER_IMAGE_WORKSPACE_DIR = Constant(default=None)
    AWS_LAMBDA_TEST_DOCKER_IMAGE = Constant(default=None)

    def ensure_aws_lambda_deploy_s3_bucket(self):
        self.ensure_attr_not_none(self.AWS_LAMBDA_DEPLOY_S3_BUCKET.name)


class RepoConfig(
    _RepoConfig,
    _DocConfig,
    _AWSLambdaConfig,
):
    DIR_CWD = Derivable(cache=True)

    @DIR_CWD.getter
    def get_DIR_CWD(self):
        """
        By default, it is where you originally call this script.

        let's say you are at ``/here`` and you have ``a.sh`` and ``b.py``::

            /
            /first/a.sh
            /first/second/b.py

        If you made a ``bash ./first/a.sh`` and ``a.sh`` actually calls
        ``python /first/second/b.py``. You will see the ``os.getcwd()`` still
        returns the corret dir where you initially run the bash command in ``b.py``
        """
        return os.getcwd()

    IS_PYGITREPO_DIR = Derivable(cache=True)

    @IS_PYGITREPO_DIR.getter
    def get_IS_PYGITREPO_DIR(self):
        return os.path.exists(
            os.path.join(
                self.DIR_CWD.get_value(),
                constants.PYGITREPO_CONFIG_FILE
            )
        )

    def read_pygitrepo_config_file(self):
        p = os.path.join(
            self.DIR_CWD.get_value(),
            constants.PYGITREPO_CONFIG_FILE
        )
        with open(p, "rb") as f:
            json_content = f.read().decode("utf-8")
            config_data = json.loads(strip_comments(json_content))
        self.update(config_data)

    DIR_HOME = Derivable(cache=True)

    @DIR_HOME.getter
    def get_DIR_HOME(self):
        return os.path.expanduser("~")

    # === Code File Structure
    # --- python project basics
    @property
    def dir_project_root(self):
        return self.DIR_CWD.get_value()

    @property
    def path_readme(self):
        return os.path.join(self.dir_project_root, "README.rst")

    @property
    def dir_python_lib(self):
        return os.path.join(self.dir_project_root, self.PACKAGE_NAME.get_value())

    @property
    def path_version_file(self):
        return os.path.join(self.dir_python_lib, "_version.py")

    @property
    def package_version(self):
        sys.path.append(self.dir_python_lib)
        try:
            from _version import __version__
            return __version__
        except:
            return constants.UNKNOWN

    @property
    def path_requirements_file(self):
        return os.path.join(self.dir_project_root, "requirements.txt")

    @property
    def path_requirements_dev_file(self):
        return os.path.join(self.dir_project_root, "requirements-dev.txt")

    @property
    def path_requirements_doc_file(self):
        return os.path.join(self.dir_project_root, "requirements-doc.txt")

    @property
    def path_requirements_test_file(self):
        return os.path.join(self.dir_project_root, "requirements-test.txt")

    @property
    def dir_pypi_build(self):
        return os.path.join(self.dir_project_root, "build")

    @property
    def dir_pypi_distribute(self):
        return os.path.join(self.dir_project_root, "dist")

    @property
    def dir_pypi_egg(self):
        return os.path.join(
            self.dir_project_root,
            "{}.egg-info".format(self.PACKAGE_NAME.get_value())
        )

    @property
    def path_fix_code_style_script(self):
        return os.path.join(self.dir_project_root, "fix_code_style.py")

    # --- testing
    @property
    def dir_tests(self):
        return os.path.join(self.dir_project_root, "tests")

    @property
    def dir_unit_tests(self):
        return self.dir_tests

    @property
    def dir_integration_tests(self):
        return os.path.join(self.dir_project_root, "tests_integration")

    @property
    def dir_pytest_cache(self):
        return os.path.join(self.dir_project_root, ".pytest_cache")

    @property
    def dir_codecov_yml(self):
        return os.path.join(self.dir_project_root, "codecov.yml")

    @property
    def path_coverage_config(self):
        return os.path.join(self.dir_project_root, ".coveragerc")

    @property
    def dir_coverage_annotate(self):
        return os.path.join(self.dir_project_root, ".coverage.annotate")

    @property
    def dir_pyenv_local_versions_for_tox(self):
        try:
            return " ".join(self.TOX_TEST_VERSIONS.get_value())
        except:
            return constants.UNKNOWN

    @property
    def dir_tox_cache(self):
        return os.path.join(self.dir_project_root, ".tox")

    # --- sphinx doc
    @property
    def dir_sphinx_doc(self):
        return os.path.join(self.dir_project_root, "docs")

    @property
    def dir_sphinx_doc_source(self):
        return os.path.join(self.dir_sphinx_doc, "source")

    @property
    def dir_sphinx_doc_source_conf_py(self):
        return os.path.join(self.dir_sphinx_doc_source, "conf.py")

    @property
    def dir_sphinx_doc_build(self):
        return os.path.join(self.dir_sphinx_doc, "build")

    @property
    def dir_sphinx_doc_build_html(self):
        return os.path.join(self.dir_sphinx_doc_build, "html")

    @property
    def path_sphinx_doc_build_html_index(self):
        return os.path.join(self.dir_sphinx_doc_build_html, "index.html")

    @property
    def path_readthedocs_yml(self):
        return os.path.join(self.dir_project_root, "readthedocs.yml")

    @property
    def url_rtd_doc(self):
        return "https://{}.readthedocs.io/".format(self.DOC_HOST_RTD_PROJECT_NAME.get_value())

    @property
    def url_s3_doc_latest(self):
        """
        The document website url for latest doc on s3.
        """
        return "https://{bucket}.s3.amazonaws.com/docs/{package_name}/latest/index.html".format(
            bucket=self.DOC_HOST_S3_BUCKET.get_value(),
            package_name=self.PACKAGE_NAME.get_value(),
        )

    @property
    def url_s3_doc_versioned(self):
        """
        The document website url for versioned doc on s3.
        """
        return "https://{bucket}.s3.amazonaws.com/docs/{package_name}/{version}/index.html".format(
            bucket=self.DOC_HOST_S3_BUCKET.get_value(),
            package_name=self.PACKAGE_NAME.get_value(),
            version=self.package_version,
        )

    @property
    def s3_uri_doc_dir_latest(self):
        return "s3://{bucket}/docs/{package_name}/latest".format(
            bucket=self.DOC_HOST_S3_BUCKET.get_value(),
            package_name=self.PACKAGE_NAME.get_value(),
        )

    @property
    def s3_uri_doc_dir_versioned(self):
        return "s3://{bucket}/docs/{package_name}/{version}/".format(
            bucket=self.DOC_HOST_S3_BUCKET.get_value(),
            package_name=self.PACKAGE_NAME.get_value(),
            version=self.package_version,
        )

    # === Pyenv
    @property
    def path_bin_global_python(self):
        if IS_WINDOWS:
            return "/c/Python{}.{}/python.exe".format(self.DEV_PY_VER_MAJOR, self.DEV_PY_VER_MINOR)
        elif IS_MACOS or IS_LINUX:
            return os.path.join(
                self.DIR_HOME.get_value(),
                ".pyenv",
                "shims",
                "python{}.{}".format(
                    self.DEV_PY_VER_MAJOR.get_value(),
                    self.DEV_PY_VER_MINOR.get_value(),
                )
            )
        else:
            raise EnvironmentError

    # === Virtualenv
    @property
    def venv_name(self):
        return "{}_venv".format(self.PACKAGE_NAME.get_value())

    @property
    def dir_all_python_versioned_venv(self):
        if IS_WINDOWS or IS_MACOS or IS_LINUX:
            return os.path.join(
                self.DIR_HOME.get_value(),
                "venvs",
                "python",
                "{}.{}.{}".format(
                    self.DEV_PY_VER_MAJOR.get_value(),
                    self.DEV_PY_VER_MINOR.get_value(),
                    self.DEV_PY_VER_MICRO.get_value(),
                ),
            )
        else:
            raise ValueError

    @property
    def dir_venv(self):
        return os.path.join(self.dir_all_python_versioned_venv, self.venv_name)

    @property
    def dir_venv_site_packages(self):
        if IS_WINDOWS:
            return os.path.join(self.dir_venv, "Lib", "site-packages")
        elif IS_MACOS or IS_LINUX:
            return os.path.join(
                self.dir_venv,
                "lib",
                "python{}.{}".format(
                    self.DEV_PY_VER_MAJOR.get_value(),
                    self.DEV_PY_VER_MINOR.get_value()
                ),
                "site-packages",
            )
        else:
            raise Exception

    @property
    def dir_venv_site_packages_64(self):
        if IS_WINDOWS:
            return os.path.join(self.dir_venv, "Lib64", "site-packages")
        elif IS_MACOS or IS_LINUX:
            return os.path.join(
                self.dir_venv,
                "lib64",
                "python{}.{}".format(
                    self.DEV_PY_VER_MAJOR.get_value(),
                    self.DEV_PY_VER_MINOR.get_value()),
                "site-packages",
            )
        else:
            raise Exception

    @property
    def dir_venv_site_packages_INSTALLED(self):
        return os.path.join(
            self.dir_venv_site_packages,
            self.PACKAGE_NAME.get_value()
        )

    @property
    def dir_venv_site_packages_egg_link(self):
        return os.path.join(
            self.dir_venv_site_packages,
            "{}.egg-link".format(self.package_name_slugify)
        )

    # --- venv/bin
    @property
    def dir_venv_bin(self):
        if IS_WINDOWS:
            return os.path.join(self.dir_venv, "Scripts")
        elif IS_MACOS or IS_LINUX:
            return os.path.join(self.dir_venv, "bin")
        else:
            raise Exception

    @property
    def path_venv_bin_python(self):
        return os.path.join(self.dir_venv_bin, "python")

    @property
    def path_venv_bin_pip(self):
        return os.path.join(self.dir_venv_bin, "pip")

    @property
    def path_venv_bin_activate(self):
        return os.path.join(self.dir_venv_bin, "activate")

    @property
    def path_venv_bin_pytest(self):
        return os.path.join(self.dir_venv_bin, "pytest")

    @property
    def path_venv_bin_sphinx_quickstart(self):
        return os.path.join(self.dir_venv_bin, "sphinx-quickstart")

    @property
    def path_venv_bin_twine(self):
        return os.path.join(self.dir_venv_bin, "twine")

    @property
    def path_venv_bin_tox(self):
        return os.path.join(self.dir_venv_bin, "tox")

    @property
    def path_venv_bin_jupyter(self):
        return os.path.join(self.dir_venv_bin, "jupyter")

    @property
    def path_venv_bin_ansible(self):
        return os.path.join(self.dir_venv_bin, "ansible")

    @property
    def path_venv_bin_aws(self):
        return os.path.join(self.dir_venv_bin, "aws")

    @property
    def path_venv_bin_chalice(self):
        return os.path.join(self.dir_venv_bin, "chalice")

    @property
    def path_venv_bin_flask(self):
        return os.path.join(self.dir_venv_bin, "flask")

    @property
    def path_venv_bin_configirl(self):
        return os.path.join(self.dir_venv_bin, "configirl")

    # === AWS CLI
    @property
    def aws_cli_profile_arg_doc_host(self):
        doc_host_aws_profile = self.DOC_HOST_AWS_PROFILE.get_value()
        if doc_host_aws_profile is None:
            return ""
        else:
            return doc_host_aws_profile

    @property
    def aws_cli_profile_arg_lambda_deploy(self):
        aws_lambda_deploy_aws_profile = self.AWS_LAMBDA_DEPLOY_AWS_PROFILE.get_value()
        if aws_lambda_deploy_aws_profile is None:
            return ""
        else:
            return aws_lambda_deploy_aws_profile

    # ==========================================================================
    # AWS Lambda
    # ==========================================================================
    # --- local ---
    @property
    def dir_lambda_build(self):
        return os.path.join(self.dir_pypi_build, "lambda")

    @property
    def path_lambda_build_source(self):
        return os.path.join(self.dir_lambda_build, "source.zip")

    @property
    def path_lambda_build_layer(self):
        return os.path.join(self.dir_lambda_build, "layer.zip")

    @property
    def path_lambda_build_deploy_package(self):
        return os.path.join(self.dir_lambda_build, "deploy-pkg.zip")

    # --- s3 ---
    @property
    def s3_key_lambda_deploy_dir(self):
        """
        example: lambda/my_package/
        """
        return s3_key_smart_join(
            parts=[
                "lambda",
                self.PACKAGE_NAME.get_value(),
            ],
            is_dir=True,
        )

    @property
    def s3_key_lambda_deploy_versioned_dir(self):
        """
        example: lambda/my_package/0.0.1/
        """
        return s3_key_smart_join(
            parts=[
                self.s3_key_lambda_deploy_dir,
                self.package_version,
            ],
            is_dir=True,
        )

    @property
    def s3_uri_lambda_deploy_versioned_dir(self):
        """
        example: s3://bucket/lambda/my_package/0.0.1/
        """
        self.ensure_aws_lambda_deploy_s3_bucket()
        return join_s3_uri(
            bucket=self.AWS_LAMBDA_DEPLOY_S3_BUCKET.get_value(),
            key=self.s3_key_lambda_deploy_versioned_dir,
        )

    # --- versioned source
    @property
    def s3_key_lambda_deploy_versioned_source_dir(self):
        """
        example: lambda/my_package/0.0.1/source/
        """
        return s3_key_smart_join(
            parts=[
                self.s3_key_lambda_deploy_versioned_dir,
                "source",
            ],
            is_dir=True,
        )

    @property
    def s3_uri_lambda_deploy_versioned_source_dir(self):
        """
        example: s3://bucket/lambda/my_package/0.0.1/source/
        """
        self.ensure_aws_lambda_deploy_s3_bucket()
        return join_s3_uri(
            bucket=self.AWS_LAMBDA_DEPLOY_S3_BUCKET.get_value(),
            key=self.s3_key_lambda_deploy_versioned_source_dir,
        )

    # --- versioned layer
    @property
    def s3_key_lambda_deploy_versioned_layer_dir(self):
        """
        example: lambda/my_package/0.0.1/layer/
        """
        return s3_key_smart_join(
            parts=[
                self.s3_key_lambda_deploy_versioned_dir,
                "layer",
            ],
            is_dir=True,
        )

    @property
    def s3_uri_lambda_deploy_versioned_layer_dir(self):
        """
        example: s3://bucket/lambda/my_package/0.0.1/layer/
        """
        self.ensure_aws_lambda_deploy_s3_bucket()
        return join_s3_uri(
            bucket=self.AWS_LAMBDA_DEPLOY_S3_BUCKET.get_value(),
            key=self.s3_key_lambda_deploy_versioned_layer_dir,
        )

    # --- versioned deploy package
    @property
    def s3_key_lambda_deploy_versioned_deploy_pkg_dir(self):
        """
        example: lambda/my_package/0.0.1/deploy-pkg/
        """
        return s3_key_smart_join(
            parts=[
                self.s3_key_lambda_deploy_versioned_dir,
                "deploy-pkg",
            ],
            is_dir=True,
        )

    @property
    def s3_uri_lambda_deploy_versioned_deploy_pkg_dir(self):
        """
        example: s3://bucket/lambda/my_package/0.0.1/deploy-pkg/
        """
        self.ensure_aws_lambda_deploy_s3_bucket()
        return join_s3_uri(
            bucket=self.AWS_LAMBDA_DEPLOY_S3_BUCKET.get_value(),
            key=self.s3_key_lambda_deploy_versioned_deploy_pkg_dir,
        )

    @property
    def layer_name(self):
        return self.PACKAGE_NAME.get_value()

    @property
    def url_lambda_layer_console(self):
        return "https://console.aws.amazon.com/lambda/home?#/layers/{layer_name}".format(
            layer_name=self.layer_name
        )
