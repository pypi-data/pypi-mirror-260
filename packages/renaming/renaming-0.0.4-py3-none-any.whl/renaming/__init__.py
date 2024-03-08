import os
import re
import functools

import consoleiotools as cit
import consolecmdtools as cct
for lib in (libs := ['tomllib', 'tomli']):
    try:
        toml_parser = __import__(lib)
        break
    except ImportError:
        pass
else:
    raise ImportError("No TOML parser lib found in {libs}!")


__version__ = "0.0.4"


CONFIG_FILENAME = 'renaming.toml'  # the default config file name


def _soft_raise(text: str):
    """Print the error message, pause the program and exit."""
    cit.err(text)
    cit.pause()
    cit.bye()


def parse_config(path: str = CONFIG_FILENAME, folder: str = os.getcwd()) -> dict:
    """Parse the config file.

    Args:
        path (str): The path or the file name of the config file.
        folder (str): The folder path of the config file. Default is the current working directory.

    Returns:
        dict: The config dict.
    """
    config_path: cct.Path = cct.get_path(path)
    if os.path.isabs(config_path):
        if not config_path.exists:
            _soft_raise(f"Config file not found: {config_path}")
    else:
        return parse_config(os.path.join(cct.get_path(folder), config_path))
    with open(config_path, 'rb') as fl:
        config = toml_parser.load(fl)
    if not config:
        _soft_raise(f"Config file is empty: {config_path}")
    if config.get('renaming') is None:
        _soft_raise(fr"Config file is missing the `\[renaming]` section: {config_path}")
    if not config.get('renaming').get('old'):
        _soft_raise(fr"Config file is missing the `old=` in the `\[renaming]` section: {config_path}")
    if not config.get('renaming').get('new'):
        _soft_raise(fr"Config file is missing the `new=` in the `\[renaming]` section: {config_path}")
    if config.get('vars') is None and config.get('patterns') is None:
        _soft_raise(fr"Config file is missing both `\[vars]` and `\[patterns]` sections: {config_path}")
    if not config.get('vars') and not config.get('patterns'):
        _soft_raise(fr"Config file is empty both `\[vars]` and `\[patterns]` sections: {config_path}")
    return config


def validate_filename(path: str, pattern: str) -> bool:
    """Validate the file name."""
    filepath = cct.get_path(path)
    if re.match(pattern, filepath.basename):
        return True
    else:
        return False


def run_renaming(config_path: str, folder: str, dry_run: bool = False):
    """Run the renaming process.

    Args:
        config_path (str): The path or the file name of the config file.
        folder (str): The folder path of the config file. Default is the current working directory.
        dry_run (bool): Dry run mode. Default is False.
    """
    if not config_path:
        config_path = CONFIG_FILENAME
    if not folder:
        folder = os.getcwd()
    cit.info(f"Folder: {folder}")
    cit.info(f"Config: {config_path}")
    config: dict = parse_config(config_path, folder)
    rename_count: int = 0
    vars: dict = {}
    validator = functools.partial(validate_filename, pattern=config["renaming"]["old"])
    cct.ls_tree(folder, to_visible=validator)
    if dry_run:
        cit.warn("[DRY-RUN] No file will be actually renamed.")
    for path in cct.get_paths(folder, filter=validator):
        path = cct.get_path(path)
        if static_vars := config.get("vars"):
            vars.update(static_vars)
        if patterns := config.get("patterns"):
            for var, pattern in patterns.items():
                if matchs := re.match(pattern, path.basename):
                    vars[var] = "".join(matchs.groups())
                else:
                    cit.warn(f"Pattern `{pattern}` not matched in `{path.basename}`")
        for i in range(1, 99):
            try:
                new_filename = config["renaming"]["new"].format(**vars, i=i)
            except KeyError as e:
                _soft_raise(fr"New filename pattern KeyError: Key {e} not found in `{config["renaming"]["new"]}` both `\[vars]` and `\[patterns]` sections.")
            new_filepath = os.path.join(path.parent, new_filename)
            if not cct.get_path(new_filepath).exists:
                if not dry_run:
                    cct.move_file(path, new_filepath)
                cit.info(f"Renamed: `[u]{path.basename}[/]` => `[u]{new_filename}[/]`")
                rename_count += 1
                break
        else:
            cit.warn("Too many files with the same date.")
    cit.panel(f"Renamed {rename_count} files.", expand=False)
