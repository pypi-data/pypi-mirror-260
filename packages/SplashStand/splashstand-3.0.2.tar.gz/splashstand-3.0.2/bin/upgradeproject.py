from contextlib import suppress
from os import chdir
from pathlib import Path
from shutil import copy2
from shutil import copytree
from shutil import ignore_patterns
from shutil import rmtree
from subprocess import run
import typing as t

from click import command
from click import help_option
from click import option
from requests import get

from .startproject import backup_dir
from .startproject import basedir
from .startproject import reset_debug
from .startproject import whiskey_dir
from acb.actions.encode import load

for f in "pprint":
    ...

restore_dirs = ["plugins"]
restore_files = ["base.yml", "mail.yml", "exclude.yml"]
ignore = ["__pycache__", ".DS_Store"] + restore_dirs + restore_files
core_plugins = ["__init__.py", "imports.py", "imports.yml", "contacts.py"]


def upgrade_project(app_name: str, deploy: bool = False) -> None:
    app_dir = basedir / app_name
    tmp_dir = app_dir / "tmp"
    migrations_dir = tmp_dir / "migrations"
    backup = backup_dir / f"{app_name}.bak"
    backup2 = backup_dir / f"{app_name}.bak2"
    with suppress(FileNotFoundError):
        rmtree(str(backup2.resolve()))
    if backup.exists():
        copytree(backup, backup2)
        rmtree(str(backup.resolve()))
    template = "fender"
    ignore.append(template)
    copytree(app_dir, backup)
    rmtree(str(app_dir.resolve()))
    copytree(whiskey_dir, app_dir, ignore=ignore_patterns(*ignore))
    for d in restore_dirs + [Path("templates") / template]:
        print("Restoring: ", d)
        with suppress(FileNotFoundError):
            copytree(backup / d, app_dir / d)
    for file in restore_files:
        print("Restoring: ", file)
        with suppress(FileNotFoundError):
            copy2(backup / file, app_dir / file)
    whiskey_plugins = whiskey_dir / "plugins"
    app_plugins = app_dir / "plugins"
    for f in core_plugins:
        print("Upgrading plugin: ", f)
        plugin_file = app_plugins / f
        copy2(whiskey_plugins / f, plugin_file)
    rmtree(migrations_dir)
    chdir(app_dir)
    run("python upgrade.py".split())
    if deploy:
        reset_debug(app_dir)
        base_settings = load.yaml(app_dir / "base.yml")
        domain = base_settings["domain"]
        run("python deploy.py".split())
        # add_custom_domain(app_name, domain)
        with suppress(Exception):
            for d in (domain, f"{domain}/admin"):
                print(f"Fetching {d}...")
                resp = get(f"https://{d}", timeout=60)
                print(resp, "\n")
        # get_revisions(app_name)
    chdir(basedir)


def upgrade_template(app_name: str, path: Path) -> None:
    path = Path(path)
    app_dir = basedir / app_name
    src = whiskey_dir / path
    dest = app_dir / path
    print(f"Copying {'/'.join(src.parts[-4:])} to {'/'.join(dest.parts[-4:])}")
    print(src.parts, dest.parts)
    print("debugging...not copied.")
    # copy2(src, dest)


@command()
@help_option("-h", is_flag=True, help="help")
@option("-a", help="upgrade project: -a [app_name]")
@option("-x", help="exclude project: -x [app_name]")
@option("-d", is_flag=True, help="deploy to gcloud")
@option("-t", nargs=2, help="upgrade theme file: -t [app_name] [file]")
def upgradeproject(a: str, t: list[str], d: bool, x: t.Optional[str] = None) -> None:
    all_apps = [a.name for a in basedir.iterdir()]
    if a:
        if a == "all":
            for app in all_apps:
                if app == x:
                    continue
                print(f"Upgrading:  {app}")
                upgrade_project(app, d)
        else:
            upgrade_project(a.rstrip("/"), d)
    elif t:
        if t[0] == "all":
            for app in all_apps:
                print(f"Upgrading:  {app} - {t[1]}")
                upgrade_template(app, Path(t[1]))
        else:
            upgrade_template(t[0].rstrip("/"), Path(t[1]))
