# -*- coding: utf-8 -*-

"""
This module implements the ``pygitrepo`` Python development workflow
best practice logics.
"""

from __future__ import print_function, unicode_literals

try:
    import typing
except ImportError:  # pragma: no cover
    pass

import os
import shutil
import subprocess
import functools
from zipfile import ZipFile

from .pkg.mini_six import input
from .pkg.fingerprint import fingerprint
from .repo_config import RepoConfig
from .operation_system import (
    IS_WINDOWS, IS_MACOS, IS_LINUX,
    OPEN_COMMAND
)
from .helpers import (
    remove_if_exists, makedir_if_not_exists,
    join_s3_uri,
    split_s3_uri,
    make_s3_console_url,
    s3_uri_to_url,
    s3_key_smart_join,
    ensure_s3_dir,
    copy_python_code,
)
from .color_print import (
    Fore, Style, TAB,
    pgr_print, pgr_print_done, print_path, print_line, colorful_path,
)


def subcommand(
    name=None,
    help=None,
):
    """
    A decorator that mark a function / class method a sub command for CLI.

    :type name: str
    :type help: str
    """

    def real_deco(func):
        if name is None:
            func._subcommand_name = func.__name__.replace("_", "-")
        else:
            func._subcommand_name = name.replace("_", "-")
        func._subcommand_help = help
        func._is_subcommand = True

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            return res

        return wrapper

    return real_deco


class Actions(object):
    """
    A class container that includes ``pgr`` CLI interface logic.
    Each command method wrapped with a :func:`subcommand` decorator is a
    underlying logic for ``pgr ${subcommand}``.

    Usually each function has a ``**kwargs`` optional keyword arguments.
    It can be used to store optional command line arguments.
    """

    # ==============================================================================
    # Python Package Development Related
    # ==============================================================================
    @subcommand(
        help="** Create virtualenv for python package development.",
    )
    def venv_up(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}create a virtualenv at {reset}{dir_venv}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                dir_venv=config.dir_venv,
            )
        )
        if os.path.exists(config.dir_venv):
            pgr_print(
                "{cyan}{tab}skip, virtualenv directory already exists!".format(
                    cyan=Fore.CYAN,
                    tab=TAB,
                )
            )
        else:
            if _dry_run is False:
                # call the global virtualenv command
                subprocess.call([
                    "virtualenv",
                    "-p",
                    config.path_bin_global_python,
                    config.dir_venv,
                ])
                # call pip install command
                subprocess.call([
                    config.path_venv_bin_pip,
                    "install",
                    "--upgrade",
                    "pip",
                ])
            pgr_print_done(indent=1)

    @subcommand(
        help="** Remove the virtualenv for this project.",
    )
    def venv_remove(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}remove virtualenv at {reset}{dir_venv}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                dir_venv=config.dir_venv,
            )
        )
        if os.path.exists(config.dir_venv):
            if _dry_run is False:
                remove_if_exists(config.dir_venv)
            pgr_print_done(indent=1)
        else:
            pgr_print(
                "{cyan}{tab}skip, virtualenv directory doesn't exists!".format(
                    cyan=Fore.CYAN,
                    tab=TAB,
                )
            )

    @subcommand(
        help="** Clean temp files.",
    )
    def clean(
        self,
        config,
        ignore_tox=False,
        _dry_run=False,
        **kwargs
    ):
        """
        :type config: RepoConfig
        """
        pgr_print("{cyan}remove all temp files ...".format(cyan=Fore.CYAN))

        to_delete = [
            config.dir_pypi_build,
            config.dir_sphinx_doc_build,
            config.dir_coverage_annotate,
            config.dir_pytest_cache,
        ]

        if ignore_tox is False:
            to_delete.append(config.dir_tox_cache)

        for p in to_delete:
            pgr_print(
                "{cyan}  clean {reset}{path} {cyan}...".format(
                    cyan=Fore.CYAN,
                    reset=Style.RESET_ALL,
                    path=p,
                )
            )
            if _dry_run is False:
                remove_if_exists(p)

        pgr_print_done(indent=1)

    @subcommand(
        help="Uninstall the package from virtualenv.",
    )
    def pip_uninstall(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}uninstall '{package_name}' from virtualenv".format(
                cyan=Fore.CYAN,
                package_name=config.PACKAGE_NAME.get_value(),
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_pip,
                "uninstall",
                "-y",
                config.PACKAGE_NAME.get_value(),
            ])
        pgr_print_done(indent=1)

    @subcommand(
        help="** Install the package to virtualenv in editable mode.",
    )
    def pip_dev_install(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self.pip_uninstall(config, _dry_run=_dry_run, **kwargs)
        pgr_print(
            "{cyan}install '{package_name}' to virtualenv in editable mode".format(
                cyan=Fore.CYAN,
                package_name=config.PACKAGE_NAME.get_value(),
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_pip,
                "install",
                "--editable",
                config.dir_project_root,
            ])
        pgr_print_done(indent=1)

    @subcommand(
        help="Install the package to virtualenv in regular mode.",
    )
    def pip_install(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self.pip_uninstall(config, _dry_run=_dry_run, **kwargs)
        pgr_print(
            "{cyan}install '{package_name}' to virtualenv".format(
                cyan=Fore.CYAN,
                package_name=config.PACKAGE_NAME.get_value(),
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_pip,
                "install",
                config.dir_project_root,
            ])
        pgr_print_done(indent=1)

    @subcommand(
        help="** Display useful information",
    )
    def info(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Display useful information, {green}path exists{cyan}, {red}path not exists".format(
                cyan=Fore.CYAN,
                green=Fore.GREEN,
                red=Fore.RED,
            )
        )
        print_path(
            "virtual environment directory",
            config.dir_venv,
        )
        print_path(
            "venv python executable path",
            config.path_venv_bin_python
        )
        print_path(
            "venv pip executable path",
            config.path_venv_bin_pip,
        )
        if IS_WINDOWS:
            print_line(
                "- {cyan}activate venv command: {path}".format(
                    cyan=Fore.CYAN,
                    path=colorful_path(config.path_venv_bin_activate),
                )
            )
        elif IS_MACOS or IS_LINUX:
            print_line(
                "- {cyan}activate venv command: source {path}".format(
                    cyan=Fore.CYAN,
                    path=colorful_path(config.path_venv_bin_activate),
                )
            )
        else:
            raise NotImplementedError

        print_line(
            "- {cyan}deactivate venv command: {reset}deactivate".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        print_path(
            "site-packages directory",
            config.dir_venv_site_packages,
        )
        print_path(
            "site-packages64 directory",
            config.dir_venv_site_packages_64,
        )

    @subcommand(
        help="** Install dev dependencies in requirements-dev.txt",
    )
    def req_dev(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}install dependencies in {reset}requirements-dev.txt to virtualenv".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_pip,
                "install",
                "-r",
                config.path_requirements_dev_file,
            ])
        pgr_print_done(indent=1)

    @subcommand(
        help="Install doc dependencies in requirements-doc.txt",
    )
    def req_doc(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}install dependencies in {reset}requirements-doc.txt to virtualenv".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_pip,
                "install",
                "-r",
                config.path_requirements_doc_file,
            ])
        pgr_print_done(indent=1)

    @subcommand(
        help="Install dev dependencies in requirements-test.txt",
    )
    def req_test(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}install dependencies in {reset}requirements-dev.txt to virtualenv".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_pip,
                "install",
                "-r",
                config.path_requirements_test_file,
            ])
        pgr_print_done(indent=1)

    @subcommand(
        help="Display requirements file content",
    )
    def req_info(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}dependencies in {reset}requirements.txt".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        print()
        subprocess.call([
            "cat",
            config.path_requirements_file,
        ])
        print()

        pgr_print(
            "{cyan}dependencies in {reset}requirements-dev.txt".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        print()
        subprocess.call([
            "cat",
            config.path_requirements_dev_file,
        ])
        print()

        pgr_print(
            "{cyan}dependencies in {reset}requirements-doc.txt".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        print()
        subprocess.call([
            "cat",
            config.path_requirements_doc_file,
        ])
        print()

        pgr_print(
            "{cyan}dependencies in {reset}requirements-test.txt".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        print()
        subprocess.call([
            "cat",
            config.path_requirements_test_file,
        ])
        print()

    @subcommand(
        name="test-only",
        help="Run unit test with pytest.",
    )
    def test_pytest_only(self, config, _dry_run=False, **kwargs):  # pragma: no cover
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Run unit test in {reset}{dir_tests}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                dir_tests=config.dir_tests,
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_pytest,
                config.dir_tests,
                "-s",
            ])
        pgr_print_done(indent=1)

    @subcommand(
        name="test",
        help="** Run unit test with pytest. Start over, reuse nothing.",
    )
    def test_pytest(self, config, _dry_run=False, **kwargs):  # pragma: no cover
        """
        :type config: RepoConfig
        """
        self.req_test(config, _dry_run=_dry_run, **kwargs)
        self.pip_dev_install(config, _dry_run=_dry_run, **kwargs)
        if _dry_run is False:
            remove_if_exists(config.dir_pytest_cache)
        self.test_pytest_only(config, _dry_run=_dry_run, **kwargs)

    @subcommand(
        name="cov-only",
        help="Run code coverage test in pytest.",
    )
    def test_cov_only(self, config, _dry_run=False, **kwargs):  # pragma: no cover
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Run code coverage test in {reset}{dir_tests}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                dir_tests=config.dir_tests,
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_pytest,
                config.dir_tests,
                "-s",
                "--cov={}".format(config.PACKAGE_NAME.get_value()),
                "--cov-report", "term-missing",
                "--cov-report", "annotate:{}".format(config.dir_coverage_annotate),
            ])
        pgr_print_done(indent=1)

    @subcommand(
        name="cov",
        help="** Run code coverage test in pytest. Start over, reuse nothing.",
    )
    def test_cov(self, config, _dry_run=False, **kwargs):  # pragma: no cover
        """
        :type config: RepoConfig
        """
        self.req_test(config, _dry_run=_dry_run, **kwargs)
        self.pip_dev_install(config, _dry_run=_dry_run, **kwargs)
        if _dry_run is False:
            remove_if_exists(config.dir_pytest_cache)
            remove_if_exists(config.dir_coverage_annotate)
        self.test_cov_only(config, _dry_run=_dry_run, **kwargs)

    @subcommand(
        name="tox-only",
        help="Run matrix test in tox with pytest",
    )
    def test_tox_only(self, config, _dry_run=False, **kwargs):  # pragma: no cover
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Run matrix test with tox settings in {reset}tox.ini".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                dir_tests=config.dir_tests,
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_tox,
                "--workdir \"{}\"".format(config.dir_project_root),
            ])
        pgr_print_done(indent=1)

    @subcommand(
        name="tox",
        help="** Run matrix test in tox with pytest. Start over, reuse nothing.",
    )
    def test_tox(self, config, _dry_run=False, **kwargs):  # pragma: no cover
        """
        :type config: RepoConfig
        """
        self.req_test(config, _dry_run=_dry_run, **kwargs)
        self.pip_dev_install(config, _dry_run=_dry_run, **kwargs)
        if _dry_run is False:
            remove_if_exists(config.dir_tox_cache)
        self.test_tox_only(config, _dry_run=_dry_run, **kwargs)

    @subcommand(
        name="pep8",
        help="Apply pep8 (https://www.python.org/dev/peps/pep-0008/) to source code and tests.",
    )
    def reformat_pep8_code_style(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self.req_dev(config, _dry_run=_dry_run)
        pgr_print(
            "{cyan}reformat python code style, execute {reset}{reformat_script}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                reformat_script=config.path_fix_code_style_script,
            )
        )
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_python,
                config.path_fix_code_style_script,
            ])
        pgr_print_done(indent=1)

    @subcommand(
        help="Build local documents with sphinx-doc.",
    )
    def build_doc_only(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Build doc at {reset}{doc_build_html}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                doc_build_html=config.dir_sphinx_doc_build_html,
            )
        )
        if _dry_run is False:
            subprocess.call([
                "make",
                "-C", config.dir_sphinx_doc,
                "html",
            ])
        pgr_print_done(indent=1)

    @subcommand(
        help="** Build local documents with sphinx-doc, start over, reuse nothing.",
    )
    def build_doc(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self.req_doc(config, _dry_run=_dry_run, **kwargs)
        self.pip_dev_install(config, _dry_run=_dry_run, **kwargs)
        if _dry_run is False:
            remove_if_exists(config.dir_sphinx_doc_build)
            remove_if_exists(os.path.join(
                config.dir_sphinx_doc_source, config.PACKAGE_NAME.get_value()))
        self.build_doc_only(config, _dry_run=_dry_run, **kwargs)

    @subcommand(
        help="Clear recently built local documents.",
    )
    def clean_doc(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Clean recently built doc at {reset}{doc_build}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                doc_build=config.dir_sphinx_doc_build,
            )
        )
        if _dry_run is False:
            remove_if_exists(config.dir_sphinx_doc_build)
        pgr_print_done(indent=1)

    @subcommand(
        help="** View recently build local documents.",
    )
    def view_doc(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Open recently built local html doc {reset}{doc_build_html}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                doc_build_html=config.dir_sphinx_doc_build_html,
            )
        )

        if os.path.exists(
            os.path.join(config.dir_sphinx_doc_build_html, "index.html")
        ):
            path_doc_index_html = os.path.join(config.dir_sphinx_doc_build_html, "index.html")
        elif os.path.exists(
            os.path.join(config.dir_sphinx_doc_build_html, "README.html")
        ):
            path_doc_index_html = os.path.join(config.dir_sphinx_doc_build_html, "README.html")
        else:
            raise ValueError

        if _dry_run is False:
            subprocess.call([OPEN_COMMAND, path_doc_index_html])

        pgr_print_done(indent=1)

    def _deploy_doc_to_s3(
        self,
        config,
        doc_version,
        s3_uri_doc_dir,
        doc_host_aws_profile,
        _dry_run=False,
        **kwargs
    ):
        """
        Deploy local html doc to S3.

        :type config: RepoConfig

        :type doc_version: str
        :param doc_version: "latest" or "versioned"

        :type s3_uri_doc_dir: str
        :type doc_host_aws_profile: str
        """
        ensure_s3_dir(s3_uri_doc_dir)

        pgr_print(
            "{cyan}deploy doc from local to s3 as {doc_version} doc ...".format(
                cyan=Fore.CYAN,
                doc_version=doc_version,
            )
        )

        pgr_print(
            "{cyan}{tab}aws s3 rm {reset}{s3_uri_doc_dir}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                tab=TAB,
                s3_uri_doc_dir=s3_uri_doc_dir,
            )
        )
        args = [
            "aws", "s3", "rm", s3_uri_doc_dir,
            "--recursive",
            "--only-show-errors",
        ]
        if doc_host_aws_profile is not None:
            args.extend(["--profile", doc_host_aws_profile])

        if _dry_run is False:
            subprocess.call(args)

        pgr_print(
            "{cyan}{tab}aws s3 sync {reset}{dir_sphinx_doc_build_html} {s3_uri_doc_dir}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                tab=TAB,
                dir_sphinx_doc_build_html=config.dir_sphinx_doc_build_html,
                s3_uri_doc_dir=s3_uri_doc_dir,
            )
        )
        args = [
            "aws", "s3", "sync",
            config.dir_sphinx_doc_build_html, s3_uri_doc_dir,
            "--only-show-errors",
        ]
        if doc_host_aws_profile is not None:
            args.extend(["--profile", doc_host_aws_profile])

        if _dry_run is False:
            subprocess.call(args)

        s3_console_url = s3_uri_to_url(s3_uri_doc_dir)
        pgr_print(
            "{cyan}{tab}view {doc_version} doc at {reset}{s3_console_url}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                tab=TAB,
                doc_version=doc_version,
                s3_console_url=s3_console_url,
            )
        )

        pgr_print_done(indent=1)

    @subcommand(
        help="Deploy local html doc to S3 as versioned document",
    )
    def deploy_doc_to_versioned(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self._deploy_doc_to_s3(
            config,
            doc_version="versioned",
            s3_uri_doc_dir=config.s3_uri_doc_dir_versioned,
            doc_host_aws_profile=config.DOC_HOST_AWS_PROFILE.get_value(),
            _dry_run=_dry_run,
            **kwargs
        )

    @subcommand(
        help="Deploy local html doc to S3 as latest document",
    )
    def deploy_doc_to_latest(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self._deploy_doc_to_s3(
            config,
            doc_version="latest",
            s3_uri_doc_dir=config.s3_uri_doc_dir_latest,
            doc_host_aws_profile=config.DOC_HOST_AWS_PROFILE.get_value(),
            _dry_run=_dry_run,
            **kwargs
        )

    @subcommand(
        help="Deploy local html doc to S3 as versioned document, and also as latest document optionally.",
    )
    def deploy_doc(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print("{cyan}deploy doc from local to s3 ...".format(cyan=Fore.CYAN))
        self.deploy_doc_to_versioned(config, _dry_run=_dry_run, **kwargs)

        pgr_print(
            "{cyan}also deploy latest doc (y/n)?".format(
                cyan=Fore.CYAN,
                tab=TAB,
            )
        )
        entered = str(input("")).lower().strip()
        if entered in ["y", "yes"]:
            self.deploy_doc_to_latest(config, _dry_run=_dry_run, **kwargs)
        else:
            pgr_print_done(indent=1)

    @subcommand(
        name="publish",
        help="** Publish this Package to https://pypi.org/.",
    )
    def publish_to_pypi(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self.req_dev(config, _dry_run=_dry_run, **kwargs)
        self.pip_dev_install(config, _dry_run=_dry_run, **kwargs)
        pgr_print(
            "{cyan}Publish {package_name} to {reset}https://pypi.org/project/{package_name}/".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                package_name=config.PACKAGE_NAME.get_value()
            )
        )
        if _dry_run is False:
            remove_if_exists(config.dir_pypi_build)
            remove_if_exists(config.dir_pypi_distribute)
            remove_if_exists(config.dir_pypi_egg)

        cwd = os.getcwd()
        os.chdir(config.dir_project_root)
        try:
            if _dry_run is False:
                subprocess.call([
                    config.path_venv_bin_python,
                    "setup.py",
                    "sdist",
                    "bdist_wheel",
                    "--universal",
                ])
                subprocess.call([
                    config.path_venv_bin_twine,
                    "upload",
                    "dist/*",
                ])
        except:
            pass
        os.chdir(cwd)
        pgr_print_done(indent=1)

    @subcommand(
        help="Run Jupyter notebook locally.",
    )
    def run_jupyter_notebook(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print("{cyan}run jupyter notebook ...".format(cyan=Fore.CYAN))
        if _dry_run is False:
            subprocess.call([
                config.path_venv_bin_jupyter,
                "notebook",
            ])

    # ==============================================================================
    # AWS Lambda Related
    # ==============================================================================
    @subcommand(
        help="Build AWS Lambda source code zip file.",
    )
    def build_lambda_source_code(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}build lambda source code at {reset}{path}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                path=config.path_lambda_build_source
            )
        )

        # filter all python source code need to add to the zip
        to_zip_list = list()
        for dirname, _, basename_list in os.walk(config.dir_python_lib):
            # ignore __pycache__
            if dirname.endswith("__pycache__"):
                continue
            for basename in basename_list:
                # ignore .pyc, .pyo,
                if basename.endswith(".pyc") or basename.endswith(".pyo"):
                    continue
                source_path = os.path.join(dirname, basename)
                archive_path = os.path.relpath(source_path, config.dir_project_root)
                to_zip_list.append((source_path, archive_path))

        if _dry_run is False:
            makedir_if_not_exists(config.dir_lambda_build)
            remove_if_exists(config.path_lambda_build_source)

            with ZipFile(config.path_lambda_build_source, "w") as f:
                for source_path, archive_path in to_zip_list:
                    f.write(source_path, archive_path)

        pgr_print_done(indent=1)

    def _upload_lambda_zip(
        self,
        config,
        source_or_layer,
        path,
        _dry_run=False,
        **kwargs
    ):
        """
        :type config: RepoConfig
        :param source_or_layer: "source code" or "layer"
        """
        pgr_print(
            "{cyan}upload lambda {source_or_layer} from {reset}{path} {cyan}to AWS S3".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                source_or_layer=source_or_layer,
                path=path,
            )
        )
        if source_or_layer == "source code":
            s3_uri_lambda_deploy_versioned_dir = config.s3_uri_lambda_deploy_versioned_source_dir
        elif source_or_layer == "layer":
            s3_uri_lambda_deploy_versioned_dir = config.s3_uri_lambda_deploy_versioned_layer_dir
        else:
            raise ValueError

        if os.path.exists(path):
            source_md5 = fingerprint.of_file(path)
            bucket, prefix = split_s3_uri(s3_uri_lambda_deploy_versioned_dir)
            key = s3_key_smart_join(
                parts=[prefix, "{}.zip".format(source_md5)],
                is_dir=False,
            )
            s3_uri = join_s3_uri(bucket, key)
            pgr_print(
                "{cyan}{tab}upload to {reset}{s3_uri}".format(
                    cyan=Fore.CYAN,
                    tab=TAB,
                    reset=Style.RESET_ALL,
                    s3_uri=s3_uri,
                )
            )
            args = [
                "aws", "s3", "cp",
                path, s3_uri,
            ]
            aws_profile = config.AWS_LAMBDA_DEPLOY_AWS_PROFILE.get_value()
            if aws_profile is not None:
                args.extend(["--profile", aws_profile])
            if _dry_run is False:
                subprocess.call(args)
            pgr_print_done(indent=1)
        else:
            pgr_print(
                "{red}{tab}{path} {cyan}not found!".format(
                    tab=TAB,
                    red=Fore.RED,
                    cyan=Fore.CYAN,
                    path=path,
                )
            )

    @subcommand(
        help="Upload AWS Lambda source code zip file to S3.",
    )
    def upload_lambda_source_code(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self._upload_lambda_zip(
            config,
            source_or_layer="source code",
            path=config.path_lambda_build_source,
            _dry_run=_dry_run,
            **kwargs
        )

    def _find_docker(self):
        """
        Find the absolute path of the docker executable
        """
        if IS_MACOS or IS_LINUX:
            locations = [
                os.path.join("/", "usr", "bin", "docker"),
                os.path.join("/", "usr", "local", "bin", "docker"),
            ]
            for p in locations:
                if os.path.exists(p):
                    return p
            raise EnvironmentError("We cannot find docker, are you sure docker is installed?")
        else:
            raise EnvironmentError("We can only find docker bin on MacOS or Linux!")

    @subcommand(
        help="Build lambda layer using a AWS lambda runtime compatible docker image.",
    )
    def build_lambda_layer(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        config.ensure_attr_not_none(config.AWS_LAMBDA_BUILD_DOCKER_IMAGE.name)
        config.ensure_attr_not_none(config.AWS_LAMBDA_BUILD_DOCKER_IMAGE_WORKSPACE_DIR.name)
        pgr_print(
            "{cyan}build lambda layer in {reset}{docker_image} {cyan}docker container at {reset}{path}".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
                docker_image=config.AWS_LAMBDA_BUILD_DOCKER_IMAGE.get_value(),
                path=config.path_lambda_build_layer
            )
        )
        makedir_if_not_exists(config.dir_lambda_build)

        path_bin_docker = self._find_docker()
        container_only_build_lbd_layer_script_path = os.path.join(
            config.AWS_LAMBDA_BUILD_DOCKER_IMAGE_WORKSPACE_DIR.get_value(),
            "bin",
            "container-only-build-lambda-layer.sh",
        )

        if _dry_run is False:
            subprocess.call([
                path_bin_docker, "run",
                "-v", "{}:{}".format(
                    config.dir_project_root,
                    config.AWS_LAMBDA_BUILD_DOCKER_IMAGE_WORKSPACE_DIR.get_value(),
                ),
                "--rm", config.AWS_LAMBDA_BUILD_DOCKER_IMAGE.get_value(),
                "bash", container_only_build_lbd_layer_script_path,
            ])

    @subcommand(
        help="Upload AWS Lambda layer zip file to S3.",
    )
    def upload_lambda_layer(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self._upload_lambda_zip(
            config,
            source_or_layer="layer",
            path=config.path_lambda_build_layer,
            _dry_run=_dry_run,
            **kwargs
        )

    @subcommand(
        help="Deploy recently built AWS lambda layer.",
    )
    def deploy_lambda_layer(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}deploy a new version of lambda layer from AWS S3".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        if os.path.exists(config.path_lambda_build_layer):
            source_md5 = fingerprint.of_file(config.path_lambda_build_layer)
            bucket, prefix = split_s3_uri(config.s3_uri_lambda_deploy_versioned_layer_dir)
            key = s3_key_smart_join(
                parts=[prefix, "{}.zip".format(source_md5)],
                is_dir=False,
            )
            s3_console_url = make_s3_console_url(bucket=bucket, prefix=key)
            pgr_print(
                "{cyan}{tab}run {reset}'aws lambda publish-layer-version' {cyan}command, preview layer file at {reset}{s3_console_url}".format(
                    cyan=Fore.CYAN,
                    tab=TAB,
                    reset=Style.RESET_ALL,
                    s3_console_url=s3_console_url,
                )
            )
            args = [
                "aws", "lambda", "publish-layer-version",
                "--layer-name", config.aws_lambda_layer_name,
                "--description",
                "dependency layer for all functions in '{}' project".format(config.aws_lambda_layer_name),
                "--content", "S3Bucket={},S3Key={}".format(
                    config.AWS_LAMBDA_DEPLOY_S3_BUCKET.get_value(), key,
                ),
                "--compatible-runtimes", "python{}.{}".format(
                    config.DEV_PY_VER_MAJOR.get_value(),
                    config.DEV_PY_VER_MINOR.get_value()
                ),
            ]
            aws_profile = config.AWS_LAMBDA_DEPLOY_AWS_PROFILE.get_value()
            if aws_profile is not None:
                args.extend(["--profile", aws_profile])
            if _dry_run is False:
                subprocess.call(args)
            pgr_print(
                "{cyan}{tab}open {reset}{url} {cyan}to view layer".format(
                    cyan=Fore.CYAN,
                    tab=TAB,
                    reset=Style.RESET_ALL,
                    url=config.url_lambda_layer_console,
                )
            )
            pgr_print_done(indent=1)
        else:
            pgr_print(
                "{red}{tab}{path} {cyan}not found!".format(
                    tab=TAB,
                    red=Fore.RED,
                    cyan=Fore.CYAN,
                    path=config.path_lambda_build_layer,
                )
            )

    @subcommand(
        name="bud-lambda-layer",
        help="** Build, upload and deploy a new AWS lambda layer.",
    )
    def build_upload_deploy_lambda_layer(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        self.build_lambda_layer(config, _dry_run=_dry_run)
        self.upload_lambda_layer(config, _dry_run=_dry_run, **kwargs)
        self.deploy_lambda_layer(config, _dry_run=_dry_run, **kwargs)

    def _ensure_chalice_lambda_app_dir(self, config):
        """
        :type config: RepoConfig
        """
        files = [
            config.path_aws_chalice_config_json,
            config.path_aws_chalice_app_py,
        ]
        for p in files:
            if not os.path.exists(p):
                raise ValueError("{} not exists".format(p))

    @subcommand(
        help="** Deploy AWS Lambda app with AWS Chalice.",
    )
    def chalice_deploy(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Deploy AWS Lambda app with AWS Chalice".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )

        self._ensure_chalice_lambda_app_dir(config)

        # reset the ``vendor`` dir
        remove_if_exists(config.dir_aws_chalice_vendor)
        makedir_if_not_exists(config.dir_aws_chalice_vendor)

        # copy source code to ``vendor`` dir
        copy_python_code(
            config.dir_python_lib,
            config.dir_aws_chalice_vendor_source,
        )

        # invoke chalice cli
        args = [
            config.path_venv_bin_chalice,
            "--project-dir", config.dir_lambda_app,
            "deploy",
        ]
        args.extend(kwargs["_args"])
        aws_profile = config.AWS_LAMBDA_DEPLOY_AWS_PROFILE.get_value()
        if aws_profile is not None:
            args.extend(["--profile", aws_profile])

        if _dry_run is False:
            subprocess.call(args)

    @subcommand(
        help="** Delete AWS Lambda app with AWS Chalice.",
    )
    def chalice_delete(self, config, _dry_run=False, **kwargs):
        """
        :type config: RepoConfig
        """
        pgr_print(
            "{cyan}Delete AWS Lambda app with AWS Chalice".format(
                cyan=Fore.CYAN,
                reset=Style.RESET_ALL,
            )
        )
        self._ensure_chalice_lambda_app_dir(config)

        args = [
            config.path_venv_bin_chalice,
            "--project-dir", config.dir_lambda_app,
            "delete",
        ]
        args.extend(kwargs["_args"])
        aws_profile = config.AWS_LAMBDA_DEPLOY_AWS_PROFILE.get_value()
        if aws_profile is not None:
            args.extend(["--profile", aws_profile])

        if _dry_run is False:
            subprocess.call(args)


actions = Actions()
