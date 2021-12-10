# -*- coding: utf-8 -*-
import os

try:
    import typing
except:
    pass
import argparse
from pygitrepo.actions import Actions, actions
from pygitrepo.repo_config import RepoConfig
from pygitrepo.pkg.mini_colorma import Fore, Style

SUB_COMMAND = "sub_command"


def colorful(message):
    return Fore.CYAN + message + Style.RESET_ALL


parser = argparse.ArgumentParser(
    prog="pygitrepo",
)
subparser = parser.add_subparsers(
    title="sub commands",
    description="run automation script",
    prog="hello",
    dest=SUB_COMMAND,
)

# A dictionary object provide access to the underlying function using
# subcommand name
action_mapper = dict()  # type: typing.Dict[str, callable]
for method_name, method in Actions.__dict__.items():
    if not method_name.startswith("_"):
        subcommand_parser = subparser.add_parser(
            name=method._subcommand_name,
            help=Fore.CYAN + method._subcommand_help + Style.RESET_ALL
        )
        subcommand_parser.add_argument(
            "--do-dry-run",
            action="store_true",
            help="display info, doesn't take effect",
        )
        action_mapper[method._subcommand_name] = getattr(actions, method_name)


# manually add more important subc  ```````ommand parser
class AddtionalSubCommandEnum:
    get_value = None


for k in AddtionalSubCommandEnum.__dict__:
    if not k.startswith("_"):
        setattr(AddtionalSubCommandEnum, k, k.replace("_", "-"))

get_value_parser = subparser.add_parser(
    name=AddtionalSubCommandEnum.get_value,
    help=Fore.CYAN + "pass python data to shell scripts" + Style.RESET_ALL
)

get_value_parser.add_argument(dest="attr_name", type=str)


def get_value(config, attr_name):
    """
    echo the value of an attribute
    
    .. code-block:: bash
    
        dir_project_root="$(pgr get-value dir_project_root)"
    
    :type config: RepoConfig
    """
    if isinstance(getattr(RepoConfig, attr_name), property):
        print(getattr(config, attr_name))
    else:
        print(getattr(config, attr_name).get_value())


def main():  # pragma: no cover
    """
    Command Line Interface entry point.
    """
    # defined arguments stored in args, a named tuple object
    # additional undefined arguments stored in unknown
    args, unknown = parser.parse_known_args()
    print(args)
    if args.sub_command is None:
        parser.parse_args(["-h"])
        return

    repo_config = RepoConfig()
    repo_config.read_pygitrepo_config_file()

    if args.sub_command in action_mapper:
        action_mapper[args.sub_command](
            repo_config,
            _dry_run=args.do_dry_run,
            _args=unknown,
        )
    elif args.sub_command == AddtionalSubCommandEnum.get_value:
        get_value(repo_config, args.attr_name)
    else:
        raise NotImplementedError
