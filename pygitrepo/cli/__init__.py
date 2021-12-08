# -*- coding: utf-8 -*-

try:
    import typing
except:
    pass
import argparse
from ..actions import Actions, actions
from ..pkg.mini_colorma import Fore, Style


class SubCommandEnum:
    venv_up = None
    venv_remove = None
    pip_dev_install = None
    pip_install = None
    pip_uninstall = None
    req_dev = None
    req_doc = None
    req_test = None
    req_info = None
    test_pytest_only = None
    test_pytest = None
    test_cov_only = None
    test_cov = None
    test_tox_only = None
    test_tox = None
    build_doc_only = None
    build_doc = None
    deploy_doc_to_latest = None
    deploy_doc_to_versioned = None
    deploy_doc = None
    clean_doc = None
    view_doc = None
    publish_to_pypi = None
    run_jupyter_notebook = None


for k in SubCommandEnum.__dict__:
    if not k.startswith("_"):
        setattr(SubCommandEnum, k, k.replace("_", "-"))

SUB_COMMAND = "sub_command"


def colorful(message):
    return Fore.CYAN + message + Style.RESET_ALL


parser = argparse.ArgumentParser(
    prog="pygitrepo",
    # description="my description"
)

subparser = parser.add_subparsers(
    title="sub commands",
    description="run automation script",
    prog="hello",
    dest=SUB_COMMAND,
)

parser_mapper = dict() # type: typing.Dict[str, argparse.ArgumentParser]
action_mapper = dict() # type: typing.Dict[str, callable]
for method_name, method in Actions.__dict__.items():
    if not method_name.startswith("_"):
        parser_mapper[method._subcommand_name] = subparser.add_parser(
            name=method._subcommand_name,
            help=Fore.CYAN + method._subcommand_help + Style.RESET_ALL
        )
        action_mapper[method._subcommand_name] = getattr(actions, method_name)


def main():  # pragma: no cover
    """
    Command Line Interface entry point.
    """
    args = parser.parse_args()
    if args.sub_command is None:
        parser.parse_args(["-h"])
    if args.sub_command in action_mapper:
        from ..repo_config import RepoConfig
        repo_config = RepoConfig()
        repo_config.read_pygitrepo_config_file()
        action_mapper[args.sub_command](repo_config)
    else:
        raise NotImplementedError
