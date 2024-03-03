"""Generate python protobuf definitions."""

import json
import os
import pathlib
import re
import shutil
import subprocess
import tempfile

import jinja2
import tomli  # tomllib is not available in python 3.10

import corvic.version
from corvic_check import project
from corvic_check.errors import CheckError

_BUF_GENERATE_TEMPLATE = """
{
    "version": "v1",
    "plugins": [
        {"plugin": "buf.build/grpc/python:v{{grpcio_major_minor_patch}}", \
"out": {{outdir_json}} },
        {"plugin": "buf.build/protocolbuffers/python:v{{protobuf_minor_patch}}", \
"out": {{outdir_json}} },
        {"plugin": "buf.build/protocolbuffers/pyi:v{{protobuf_minor_patch}}", \
"out": {{outdir_json}} },
        {"plugin": "buf.build/community/nipunn1313-mypy-grpc:v3.5.0", \
"out": {{outdir_json}} }
    ]
}
"""


def _get_lockfile_versions(packages: list[str]) -> dict[str, corvic.version.Version]:
    with (project.root() / "poetry.lock").open(mode="rb") as f:
        obj = tomli.load(f)

    to_find = set(packages)
    versions: dict[str, corvic.version.Version] = {}
    for package in obj["package"]:
        if not to_find:
            break
        name = package["name"]
        if name in to_find:
            versions[name] = corvic.version.parse_version(package["version"])
            to_find.remove(name)

    if to_find:
        raise CheckError(f"could not find locked version for {','.join(to_find)}")
    return versions


def _buf_template_for_outdir(outdir: pathlib.Path):
    env = jinja2.Environment()
    versions = _get_lockfile_versions(["grpcio", "protobuf"])
    grpcio = versions["grpcio"]
    protobuf = versions["protobuf"]

    template = env.from_string(
        source=_BUF_GENERATE_TEMPLATE,
        globals={
            "grpcio_major_minor_patch": f"{grpcio.major}.{grpcio.minor}.{grpcio.patch}",
            "protobuf_minor_patch": f"{protobuf.minor}.{protobuf.patch}",
            "outdir_json": json.dumps(str(outdir)),
        },
    )

    return template.render()


def _fix_imports(file: pathlib.Path, gen_package_name: str, real_package_name: str):
    with file.open() as stream:
        content = stream.read()

    content = re.sub(
        rf"from {gen_package_name}(\.| )", rf"from {real_package_name}\1", content
    )

    if file.name.endswith(".pyi"):
        # the nipunn1313-mypy-grpc plugin is not as careful with imports and we need to
        # change the name of the GPRC endpoint to be corvic
        content = re.sub(rf"{gen_package_name}\.", rf"{real_package_name}.", content)

    with tempfile.NamedTemporaryFile(mode="w", dir=file.parent) as tmp_file:
        tmp_file.write(content)
        file.unlink()
        os.link(tmp_file.name, file)


def _fix_python_package(
    root: pathlib.Path, gen_package_name: str, real_package_name: str
):
    for file in root.iterdir():
        if file.is_dir():
            _fix_python_package(file, gen_package_name, real_package_name)
        elif file.is_file() and (
            file.name.endswith(".py") or file.name.endswith(".pyi")
        ):
            _fix_imports(file, gen_package_name, real_package_name)

    # add the required __init__.py file
    (root / "__init__.py").touch()


def generate():
    """Generate the corvic_generated from the protos in /proto."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = pathlib.Path(tmp_dir)
        subprocess.check_call(
            [
                "buf",
                "generate",
                "--template",
                _buf_template_for_outdir(tmp_path),
                "proto",
            ],
            cwd=project.root(),
        )
        _fix_python_package(tmp_path / "corvic", "corvic", "corvic_generated")
        corvic_generated_dir = project.root() / "python" / "corvic_generated"
        if corvic_generated_dir.exists():
            shutil.rmtree(corvic_generated_dir)
        shutil.copytree(tmp_path / "corvic", corvic_generated_dir)
