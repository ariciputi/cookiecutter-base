# pylint: disable=missing-docstring
#!/usr/bin/env python

import logging
import os
import subprocess
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def is_true(term):
    return term.lower() in ("1", "yes", "y")


def is_false(term):
    return not is_true(term)


def main():
    print("Creating the venv along with the default dependencies...")
    subprocess.run(
        ["poetry", "install"], check=True,
    )

    print("Running black on the created project...")
    subprocess.run(["poetry", "run", "black", "."], check=True)

    if is_true("{{ cookiecutter.init_git_repo }}"):
        print("Initialiazing a git repository...")
        subprocess.run(["git", "init"], check=True)

        subprocess.run(["git", "add", "--all"], check=True)
        subprocess.run(
            ["git", "commit", "--no-verify", "-m", "Initial commit"], check=True
        )

    if is_false("{{ cookiecutter.use_pre_commit }}"):
        print("Removing pre-commit conf file...")
        os.remove(os.path.join(PROJECT_DIRECTORY, ".pre-commit-config.yaml"))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pylint: disable=broad-except
        print("Post generation hook failed with the following error:")
        log.exception(exc)
        sys.exit(1)
    else:
        sys.exit(0)
