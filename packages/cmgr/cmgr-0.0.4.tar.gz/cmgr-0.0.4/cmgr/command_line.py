import os

import click

import cmgr


@click.group(invoke_without_command=True)
@click.option("-p", "--profile", "profile", default=None, help="The path of the cmgr profile file.")
@click.option("-n", "--name", "filename", default=cmgr.CMGR_PROFILE_FILENAME, help="The filename of the cmgr profile file.")
@click.option("-r", "--root", "root", default=os.getcwd(), help="The root directory to discover config manager conf files.")
@click.pass_context
def main(context: click.Context = None, profile: str = None, root: str = os.getcwd(), filename: str = cmgr.CMGR_PROFILE_FILENAME):
    if context.invoked_subcommand is None:
        if not profile:
            return cmgr.run_all_configmanager(root=root, filename=filename)
        else:
            return cmgr.run_configmanager(profile)


@main.command()
@click.argument("name", default=None)
@click.option("-c", "--command", "command", default=None, help="The command to detect the package installation.")
@click.option("-m", "--manager", "manager", default=None, help="The package manager to install the package.")
def install(name: str, command: str = None, manager: str = None):
    cmgr_info: dict = {
        "install": [
            {
                "name": name,
            }
        ],
    }
    if command:
        cmgr_info["install"][0]["command"] = command
    if manager:
        cmgr_info["install"][0]["manager"] = manager
    config_manager = cmgr.make_configmanager(cmgr_info)
    return cmgr.run_configmanager(config_manager)


@main.command()
@click.argument("src", default=None)
@click.argument("dst", default=None)
@click.option("-n", "--name", "name", default=None, help="The name of the package.")
def config(src: str, dst: str, name: str = None):
    cmgr_info: dict = {
        "config": [
            {
                "src": src,
                "dst": dst,
            }
        ],
    }
    if name:
        cmgr_info["name"] = name
    config_manager = cmgr.make_configmanager(cmgr_info)
    return cmgr.run_configmanager(config_manager)


if __name__ == "__main__":
    main()
