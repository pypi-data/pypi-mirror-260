from contextlib import suppress
from pathlib import Path
from inspect import getmodule

from .startproject import basedir
from .startproject import whiskey_dir


def get_version(version_file: Path):
    return getmodule(".".join(str(version_file.parts))).get("__version__")


def checkversions() -> None:
    print(f"\n{'whiskey': <10}{get_version(whiskey_dir / '_version.py'): >16}")

    for app in basedir.iterdir():
        if app.suffix == ".bak":
            continue
        print(f"\n{app.name: <10}", end="")
        with suppress(SyntaxError):
            version = get_version(app / "_version.py")
            # print(f"{app.name} - {version}", end="")
            print(f"{version: >16}", end="")
    print("\n")


if __name__ == "__main__":
    checkversions()
