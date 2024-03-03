"""Generate and manage python typestubs (pyi files)."""

import os
import pathlib
import re
import shutil
import subprocess
import tempfile
from collections.abc import Mapping
from typing import Any, cast

import tomli

from corvic_check import project

from .errors import CheckError


def _get_stub_dir() -> pathlib.Path:
    pyproject_file = project.root() / "pyproject.toml"

    with pyproject_file.open(mode="rb") as file:
        doc = tomli.load(file)

    tool_table = cast(Mapping[str, Any], doc["tool"])
    pyright_table = cast(Mapping[str, str], tool_table["pyright"])
    stub_dir = pyright_table["stubPath"] or "typings"

    return project.root() / stub_dir


def _set_arbitrary_creation_time(path: pathlib.Path) -> None:
    arbitrary_timestamp = 1697784423
    for root, _, files in os.walk(path):
        file_paths = [pathlib.Path(root, file) for file in files]
        for file_path in file_paths:
            os.utime(file_path, (arbitrary_timestamp, arbitrary_timestamp))


def _run_format_checks(*paths: str | pathlib.Path):
    subprocess.call(["ruff", "format", "--silent", *paths], cwd=project.root())


def generate(diff_dir: pathlib.Path, packages: list[str]):
    """Generate typestubs."""
    if packages:
        diff_files = [diff_dir / f"{package}.diff" for package in packages]
    else:
        diff_files = list(diff_dir.glob("*.diff"))

    stub_dir = _get_stub_dir()

    if stub_dir.exists():
        shutil.rmtree(stub_dir)

    # Modules may have mutual dependencies, so ensure a consistent
    # generation order by sorting and generating all before diffing.
    for file in sorted(diff_files):
        module = file.name.removesuffix(".diff")
        module_dir = stub_dir / pathlib.Path(module.replace(".", "/"))
        # Modules may have mutual dependencies, delete if already partially
        # generated.
        if module_dir.exists():
            shutil.rmtree(module_dir)
        subprocess.check_call(
            ["pyright", "-p", project.root() / "pyproject.toml", "--createstub", module]
        )

    _run_format_checks(stub_dir)

    for file in diff_files:
        subprocess.check_call(
            ["patch", "--no-backup-if-mismatch", "-p0", "-i", file], cwd=project.root()
        )


def _strip_timestamps_from_diff_output(diff_output: str) -> str:
    return re.sub(
        r"^((?:[-]{3}|[+]{3}) .+?)\s+\d+-\d+-\d+ \d+:\d+:\d+(?:\.\d+ [+-]?\d{4})?$",
        r"\1",
        diff_output,
        flags=re.MULTILINE,
    )


def sync(diff_dir: pathlib.Path, packages: list[str]):
    """Update typestub diffs."""
    if packages:
        diff_files = [diff_dir / f"{package}.diff" for package in packages]
    else:
        diff_files = list(diff_dir.glob("*.diff"))

    stub_dir = _get_stub_dir()
    rel_stub_dir = stub_dir.relative_to(project.root())

    pyproject_file = project.root() / "pyproject.toml"

    # We would like diffs to be computed wrt sibling directories but "pyright
    # --createstub -p <file or dir>" seems to partially ignore user-defined
    # files but honor user-defined directories. Instead, create the following
    # structure:
    #
    #   /fresh_dir/stub_dir
    #   /fresh_dir/stub_dir.orig -> /stub_dir
    with tempfile.TemporaryDirectory(dir=project.root()) as clean_dir:
        clean_path = pathlib.Path(clean_dir)
        clean_pyproject_file = clean_path / "pyproject.toml"
        clean_stub_path = clean_path / rel_stub_dir
        link_to_orig_stub_path = (
            clean_path / rel_stub_dir.parent / (rel_stub_dir.name + ".orig")
        )

        link_to_orig_stub_path.symlink_to(stub_dir, target_is_directory=True)

        shutil.copyfile(pyproject_file, clean_pyproject_file)

        # Modules may have mutual dependencies, so ensure a consistent
        # generation order by sorting and generating all before diffing.
        for file in sorted(diff_files):
            module = file.name.removesuffix(".diff")
            subprocess.check_call(
                ["pyright", "-p", str(clean_path), "--createstub", module]
            )

        _run_format_checks(clean_stub_path, stub_dir)
        _set_arbitrary_creation_time(stub_dir)
        _set_arbitrary_creation_time(clean_stub_path)

        for file in diff_files:
            module = file.name.removesuffix(".diff")
            subdirs = pathlib.Path(*module.split("."))

            # Modules can either be directories or files. Rather than figure
            # out if a module is really module.py, cheat a little by finding
            # the containing directory and computing a diff with respect to
            # that.
            level = -1
            candidate_dir = link_to_orig_stub_path / subdirs
            while not candidate_dir.is_dir():
                level += 1
                candidate_dir = candidate_dir.parent

            if level >= 0:
                if level >= len(subdirs.parents):
                    raise CheckError(f"could not find comparison directory for {file}")
                subdirs = subdirs.parents[level]

            clean = (clean_stub_path / subdirs).relative_to(clean_dir)
            orig = (link_to_orig_stub_path / subdirs).relative_to(clean_dir)

            diff = subprocess.run(
                ["diff", "-rNu", clean, orig],
                cwd=clean_dir,
                text=True,
                capture_output=True,
                check=False,
            )
            if diff.returncode not in (0, 1):
                raise CheckError(f"diff failed with {diff.stderr}")
            file.write_text(_strip_timestamps_from_diff_output(diff.stdout))


def create(module: str, *, diff_dir: pathlib.Path):
    """Set up a new module for typestub management."""
    diff_file = diff_dir / f"{module}.diff"
    if diff_file.exists():
        raise CheckError(f"{diff_file} already exists")
    diff_file.touch()
    subprocess.check_call(
        [
            "pyright",
            "-p",
            str(project.root() / "pyproject.toml"),
            "--createstub",
            module,
        ]
    )
    _run_format_checks(_get_stub_dir())
