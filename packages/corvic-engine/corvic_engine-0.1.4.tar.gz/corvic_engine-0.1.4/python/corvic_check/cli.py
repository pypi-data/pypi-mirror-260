"""Build tool CLI."""
import os
import pathlib
import subprocess
import sys
import webbrowser

import click
from click_default_group import DefaultGroup

from corvic_check import project, proto, python_typestubs
from corvic_check.errors import CheckError, CommandError
from corvic_check.run import run


class Profile:
    """Rust build profiles."""

    OPT_DEV = "opt-dev"
    DEBUG_RELEASE = "debug-release"

    # Work around absence of enum.StrEnum in Python < 3.11. Post 3.11 make
    # Profile a StrEnum and replace uses of values with list(Profile).
    @classmethod
    def values(cls) -> list[str]:
        """Return valid profile values."""
        return [cls.OPT_DEV, cls.DEBUG_RELEASE]


class BufErrorFormat:
    """Subset of error formats supported by buf CLI."""

    TEXT = "text"
    GITHUB_ACTIONS = "github-actions"

    # Work around absence of enum.StrEnum in Python < 3.11. Post 3.11 make
    # Profile a StrEnum and replace uses of values with list(Profile).
    @classmethod
    def values(cls) -> list[str]:
        """Return valid profile values."""
        return [cls.TEXT, cls.GITHUB_ACTIONS]


def _parse_env_bool(value: str) -> bool:
    value = value.lower().strip()

    if len(value) == 0:
        return False

    match value:
        case "true" | "1":
            return True
        case "false" | "0":
            return False
        case _:
            return True


@click.group()
def cli():
    """Build tool."""


@cli.command()
@click.option(
    "--profile", type=click.Choice(Profile.values()), default=Profile.DEBUG_RELEASE
)
@click.option(
    "--default-features/--no-default-features", default=True, show_default=True
)
@click.option("--release/--no-release", default=False, show_default=True)
def build(profile: str, default_features: bool, release: bool):
    """Make build artifacts suitable for separate installation."""
    proto.generate()
    extra: list[str] = []
    if not default_features:
        extra.append("--no-default-features")
    if release:
        extra.append("--release")
    subprocess.check_call(["maturin", "build", "--profile", profile, *extra])


@cli.command()
@click.option(
    "--profile",
    type=click.Choice(Profile.values()),
    default=Profile.OPT_DEV,
    show_default=True,
)
@click.option(
    "--default-features/--no-default-features", default=True, show_default=True
)
def dev(profile: str, default_features: bool):
    """Make build artifacts and install them into the local environment."""
    proto.generate()
    # We use [tools.poetry.scripts] to install developer tooling and maturin
    # reads [project.scripts] which is empty. Thus, the default behavior of
    # `maturin develop` to install the package will wipe the poetry installed
    # scripts.
    extra = ["--skip-install"]
    if not default_features:
        extra.append("--no-default-features")
    # Change directory to project root otherwise wrong Cargo.toml could be used
    subprocess.check_call(
        ["maturin", "develop", "--profile", profile, *extra],
        cwd=project.root(),
    )


@cli.group(cls=DefaultGroup, default="all", default_if_no_args=True)
def generate():
    """Generate code."""


@generate.command("all")
def generate_all():
    """Generate code."""
    python_typestubs.generate(project.root() / "typings", [])
    proto.generate()


@generate.command("proto")
def generate_proto():
    """Generate code from proto definitions."""
    proto.generate()


@generate.command("typestubs")
def generate_typestubs():
    """Generate pyi files.

    Type stub files are managed as diffs against pyright generated files.

    Use "typestubs sync" to convert changes on generated stubs back to a diff.

    Use "typestubs create" to set up typestubs for a new module.
    """
    python_typestubs.generate(project.root() / "typings", [])


@cli.group()
def typestubs():
    """Manage pyi files.

    Use "generate typestubs" to generate pyi files from diffs.
    """


@typestubs.command("sync")
@click.argument("modules", nargs=-1)
def typestubs_sync(modules: list[str]):
    """Convert changes on generated stubs back to a diff."""
    python_typestubs.sync(project.root() / "typings", modules)


@typestubs.command("create")
@click.argument("module")
def typestubs_create(module: str):
    """Set up typestubs for a new module."""
    python_typestubs.create(module, diff_dir=project.root() / "typings")


@cli.command()
@click.argument(
    "path",
    type=click.Path(path_type=pathlib.Path, exists=True),
    default=None,
    required=False,
)
def format(path: pathlib.Path | None):
    """Format code and files."""
    cwd = path if path else project.root()

    codes: list[int] = []
    codes.append(subprocess.call(["ruff", "format", "--silent"], cwd=cwd))
    codes.append(subprocess.call(["cargo", "fmt", "--all"], cwd=cwd))
    codes.append(subprocess.call(["dprint", "fmt", "--allow-no-files"], cwd=cwd))
    codes.append(subprocess.call(["buf", "format", "--write"], cwd=cwd))
    codes.append(
        subprocess.call(["ruff", "check", "--fix", "--exit-zero", "--silent"], cwd=cwd)
    )

    if any(codes):
        raise CommandError()


@cli.command()
@click.argument(
    "path",
    type=click.Path(path_type=pathlib.Path, exists=True),
    default=None,
    required=False,
)
@click.option(
    "--ci/--no-ci",
    default=_parse_env_bool(os.getenv("CI", "0")),
    show_default=True,
    help="If true, avoid non-determinisic checks. Default: os.environ['CI']",
)
@click.option(
    "--error-format",
    type=click.Choice(BufErrorFormat.values()),
    help="Format of error output. Currently, only applies to buf output.",
    default=BufErrorFormat.TEXT,
    required=False,
)
@click.option(
    "--against-main",
    help="Target repo to test for breaking changes.",
    default=str(project.root() / ".git"),
    required=False,
    show_default=True,
)
def lint(
    path: pathlib.Path | None, ci: bool, error_format: BufErrorFormat, against_main: str
):
    """Lint code and files."""
    cwd = path if path else project.root()

    codes: list[int] = []
    codes.append(subprocess.call(["ruff", "format", "--check"], cwd=cwd))
    codes.append(subprocess.call(["cargo", "fmt", "--check", "--all"], cwd=cwd))
    codes.append(subprocess.call(["dprint", "check"], cwd=cwd))
    codes.append(
        subprocess.call(
            [
                "buf",
                "format",
                "--diff",
                "--exit-code",
                f"--error-format={error_format}",
                project.root() / "proto",
            ],
            cwd=cwd,
        )
    )
    codes.append(
        subprocess.call(
            ["buf", "lint", f"--error-format={error_format}", project.root() / "proto"],
            cwd=cwd,
        )
    )
    codes.append(
        subprocess.call(
            [
                "buf",
                "breaking",
                f"--error-format={error_format}",
                f"--against={against_main}#subdir=proto,branch=main",
                project.root() / "proto",
            ],
            cwd=cwd,
        )
    )
    codes.append(
        subprocess.call(["lint-imports", "--config", project.root() / "pyproject.toml"])
    )
    codes.append(subprocess.call(["ruff", "check", "."], cwd=cwd))

    cargo_deny_check_args = ["bans", "licenses", "sources"]
    if not ci:
        cargo_deny_check_args += ["advisories"]

    # Change directory to project root otherwise wrong Cargo.toml could be used
    codes.append(
        subprocess.call(
            ["cargo", "deny", "check", *cargo_deny_check_args],
            cwd=project.root(),
        )
    )

    codes.append(subprocess.call(["codespell", "."], cwd=cwd))
    codes.append(
        subprocess.call(
            [
                "cargo",
                "clippy",
                "--workspace",
                "--all-targets",
                "--all-features",
                "--locked",
                "--",
                "-D",
                "warnings",
            ],
            cwd=cwd,
        )
    )
    codes.append(subprocess.check_call(["pyright"], cwd=cwd))
    if any(codes):
        raise CommandError()


@cli.group("docs", cls=DefaultGroup, default="pdoc", default_if_no_args=True)
def cli_docs():
    """Generate docs."""


@cli_docs.command("pdoc")
def cli_docs_pdoc():
    """Generate python pdoc documentation."""
    run(
        [
            "pdoc",
            "corvic",
            "-o",
            "docs/build/pdocs",
            "--docformat",
            "google",
            "--logo",
            "https://emoji.slack-edge.com/T05GSDJTX1S/corvic/90eb56550c05e709.jpg",
        ]
    )


@cli_docs.command("sphinx")
@click.option(
    "--open/--no-open",
    help="Open generated docs in browser",
    default=True,
    show_default=True,
)
@click.argument("other_sphinx_arguments", nargs=-1, type=click.UNPROCESSED)
def docs(open: bool, other_sphinx_arguments: list[str]):
    """Generate docs."""
    docs_dir = project.root() / "docs"
    subprocess.check_call(
        [
            "sphinx-build",
            "-M",
            "html",
            "source",
            "build/sphinx",
            "-W",
            *other_sphinx_arguments,
        ],
        cwd=docs_dir,
    )
    if open:
        doc_index = docs_dir / "build" / "sphinx" / "html" / "index.html"
        url = f"file://{doc_index!s}"
        webbrowser.open(url)


@cli.command()
def test():
    """Run tests."""
    subprocess.check_call(["pytest"])
    subprocess.check_call(["cargo", "test"])


def main():
    """Build tool CLI."""
    try:
        cli.main(prog_name="check")
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except CommandError:
        sys.exit(1)
    except CheckError as exc:
        sys.stderr.write(str(exc))
        sys.stderr.write("\n")
        sys.exit(1)
