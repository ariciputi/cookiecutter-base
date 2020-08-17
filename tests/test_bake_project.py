# pylint: disable=missing-docstring

import os
import subprocess
from contextlib import contextmanager


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def test_project_tree(cookies):
    project_name = "test-project"
    project_version = "1.0"

    result = cookies.bake(
        extra_context={"project_name": project_name, "version": project_version}
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == "test-project"

    src_path = result.project.join("src", "test_project")

    assert src_path.isdir()

    with inside_dir(str(result.project)):
        check_pyproject = subprocess.run(["poetry", "check"])
        assert check_pyproject.returncode == 0

        install_venv = subprocess.run(["poetry", "install"])
        assert install_venv.returncode == 0
        assert result.project.join(".venv").isdir()

        check_git = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"])
        assert check_git.returncode == 0

        check_commit = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"], capture_output=True
        )
        assert check_commit.returncode == 0
        assert check_commit.stdout.strip().decode() == "1"

        check_black = subprocess.run(["poetry", "run", "black", "--check", "."])
        assert check_black.returncode == 0

        check_name_version = subprocess.run(["poetry", "version"], capture_output=True)
        assert check_name_version.returncode == 0
        assert (
            check_name_version.stdout.strip().decode()
            == f"{project_name} {project_version}"
        )


def test_no_git_repo(cookies):
    result = cookies.bake(
        extra_context={"project_name": "test-project", "init_git_repo": "n"}
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == "test-project"

    assert not result.project.join(".git").check(dir=1)