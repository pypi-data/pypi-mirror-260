import os

import consoleiotools as cit
import consolecmdtools as cct
for lib in (libs := ['tomllib', 'tomli', 'tomlkit']):
    try:
        toml_parser = __import__(lib)
        break
    except ImportError:
        pass
else:
    raise ImportError("No TOML parser lib found in {libs}!")


__version__ = "0.0.4"


CMGR_PROFILE_FILENAME = 'cmgr.toml'  # Config Manager profile is the config file for cmgr itself.


def _soft_raise(text: str):
    """Print the error message, pause the program and exit."""
    cit.err(text)
    cit.pause()
    cit.bye()


def _parse_src_or_dst(path_or_cmd: str) -> cct.Path:
    """Parse the source or destination path or command.

    Args:
        path_or_cmd (str): The source or destination path or command.

    Returns:
        cct.Path: The parsed path.
    """
    if not path_or_cmd:
        _soft_raise("The input of `_parse_src_or_dst()` is empty!")
    if os.path.isfile(path_or_cmd):  # path_or_cmd is a file
        return cct.get_path(path_or_cmd)
    if cct.is_cmd_exist(path_or_cmd):  # path_or_cmd is a command
        return cct.get_path(cct.read_cmd(path_or_cmd).strip())
    return cct.get_path(path_or_cmd)  # path_or_cmd is not a existing file or a valid command, guess it's a file path


def print_profile_help():
    minimal_profile_url = "https://github.com/kyan001/PyConfigManager/raw/main/cmgr-minimal.toml"
    example_profile_url = "https://github.com/kyan001/PyConfigManager/raw/main/cmgr-example.toml"
    cit.info("Here is a minimal Config Manager profile example:")
    cit.print(cct.read_url(minimal_profile_url).decode())
    cit.info(f"For more details, visit: {example_profile_url}")


def ensure_packages(packages: iter) -> bool:
    """Ensure the given packages are installed.

    Args:
        packages (iter): The package infos to install. Each package info is a dict with keys: name, command (optional), manager (optional).

    Returns:
        bool: True if all packages are installed, False otherwise.
    """
    for package in packages:
        package_name = package.get('name')
        package_cmd = package.get('command') or package.get('cmd')
        package_manager = package.get('manager') or package.get('mgr')
        if cct.is_cmd_exist(package_cmd):  # if the package is already installed, nothing shown.
            continue
        cit.info(f"Installing package: {package_name}")
        if package_manager:
            result = cct.install_package(package_name, package_manager)
        else:
            result = cct.install_package(package_name)
        if not result:
            cit.err(f"Failed to install package: {package_name}!")
            return False
    return True


def get_configmanager(path: str) -> dict:
    """Get the Config Manager from the given profile file.

    Args:
        path (str): The path of the Config Manager profile file.

    Returns:
        dict: The Config Manager profile.
    """
    cmgr_profile_path = cct.get_path(path)
    if not cmgr_profile_path.exists:
        cit.warn(f"cmgr profile file `{path}` not found!")
        print_profile_help()
        cit.pause()
        cit.bye()
    with open(cmgr_profile_path, 'rb') as fl:
        cmgr_info = toml_parser.load(fl)
    if not cmgr_info:
        _soft_raise(f"Bad cmgr config file `{path}`!")
    cmgr_info['path'] = cmgr_profile_path  # add the path of the Config Manager profile to the Config Manager info.
    return make_configmanager(cmgr_info)


def make_configmanager(info: dict) -> dict:
    """Validate and calibrate the Config Manager info.

    Args:
        info (dict): The Config Manager info.

    Returns:
        dict: The calibrated Config Manager info.
    """
    if not info.get('path'):
        info['path'] = os.getcwd()
    elif not info.get('name'):
        info['name'] = info['path'].parent.basename
    if not isinstance(info.get('path'), cct.Path):
        info['path'] = cct.get_path(info.get('path'))
    if info.get('install'):
        for package in info.get('install'):
            if not package.get('name'):
                _soft_raise(f"Package name not found in {package}!")
            if not package.get('cmd'):
                package['cmd'] = package['name']
    if info.get('config'):
        for config in info.get('config'):
            if not config.get('src'):
                _soft_raise(f"Source config file path not found in {config}!")
            src = _parse_src_or_dst(config.get('src'))
            if not src.exists and not os.path.isabs(src):  # try to find the source file in the directory of the Config Manager profile.
                src = cct.get_path(os.path.join(info.get('path').parent, config.get('src')))
            if not src.exists:
                _soft_raise(f"Source config file not found: {src}!")
            config['src'] = src
            if not config.get('dst'):
                _soft_raise(f"Destination config file path not found in {config}!")
            config['dst'] = cct.get_path(_parse_src_or_dst(config.get('dst')))
            if not config.get('name'):
                config['name'] = src.basename
    if not info.get('name'):
        if info.get('config'):
            info['name'] = info['config'][0]['name']
        elif info.get('install'):
            info['name'] = info['install'][0]['name']
        else:
            info['name'] = "My Config Manager"
    return info


def discover_cmgr_confs(filename: str, root: str = None) -> list[cct.Path]:
    """Discover Config Manager profiles in the given directory or its subdirectories.

    Args:
        filename (str): The filename of the Config Manager profile.
        root (str, optional): The directory to search. If not given, the directory of this script is used.

    Returns:
        list[str]: A list of Config Manager profile paths.
    """
    if not filename:
        _soft_raise("The `filename` of Config Manager profile is empty!")
    if not root:
        root = os.getcwd()
    if not isinstance(root, cct.Path):
        root = cct.get_path(root)
    cmgr_profiles: list[cct.Path] = []
    for path in cct.bfs_walk(root):
        path = cct.get_path(path)
        if path.basename == filename:
            cmgr_profiles.append(path)
    return cmgr_profiles


def run_configmanager(config_manager: dict):
    """Run the config manager.

    Args:
        config_manager (dict): The Config Manager info.
    """
    cit.rule(f"Config Manager for {config_manager.get('name')}")
    cit.info(f"Path: {config_manager.get('path')}")
    if dependencies := config_manager.get('install'):
        cit.info(f"Dependencies: {[package.get('name') for package in dependencies]}")
    if configlets := config_manager.get("config"):
        cit.info(f"Configs: {[configlet.get('name') for configlet in configlets]}")

    # install dependencies
    if dependencies and not ensure_packages(dependencies):
        _soft_raise("Failed to install dependencies!")

    # update config files
    if configlets:
        for configlet in configlets:
            cit.start()
            cit.title(f"Configurating {configlet.get('name')}")
            cit.info(f"Source: `{configlet.get('src')}`")
            cit.info(f"Destination: `{configlet.get('dst')}`")
            src = configlet.get('src')
            dst = configlet.get('dst')
            if src.exists and dst.exists:
                diffs = cct.diff(dst, src)
                if diffs:
                    cit.info("Diff:")
                    cit.print("\n".join(diffs))
                    if cit.get_input("Update config file? (y/n)", default='y').lower() != 'y':
                        cit.warn(f"Config file for `{configlet.get('name')}` is not updated!")
                        continue
                else:
                    cit.info(f"Config file for `{configlet.get('name')}` is up-to-date!")
                    continue
            cct.copy_file(src, dst, backup=True, ensure=True, msgout=cit.info)


def run_all_configmanager(filename: str = CMGR_PROFILE_FILENAME, root: str = cct.get_path(__file__).parent):
    avail_cmgr_profiles: list[cct.Path] = discover_cmgr_confs(filename, root)
    if len(avail_cmgr_profiles) == 0:
        cit.warn("No cmgr config file found!")
    elif len(avail_cmgr_profiles) == 1 and cct.get_path(avail_cmgr_profiles[0]).parent == root:
        config_manager = get_configmanager(avail_cmgr_profiles[0])
        run_configmanager(config_manager)
    else:
        cit.ask("Which cmgr to use?")
        cmgr_conf_paths = cit.get_choices(avail_cmgr_profiles, allable=True, exitable=True)
        for cmgr_conf_path in cmgr_conf_paths:
            config_manager = get_configmanager(cmgr_conf_path)
            run_configmanager(config_manager)
    cit.pause()
