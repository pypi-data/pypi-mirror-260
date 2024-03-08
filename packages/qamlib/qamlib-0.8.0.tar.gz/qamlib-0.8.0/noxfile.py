"""Nox sessions."""
import os
import shutil
import sys
from pathlib import Path

import nox
from nox import Session
from nox import session


package = "qamlib"
python_versions = [">3.8"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = (
    "pre-commit",
    "docs-build",
)



@session(name="build")
def build(session: Session) -> None:
    """Test building of library"""
    session.install(
        "pybind11"
    )
    session.install(".")

@session(name="docs-build")
def docs_build(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["-W", "--keep-going", "docs", "docs/_build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")

    session.install(
        "sphinx",
        "breathe",
        "sphinx-autodoc-typehints",
        "furo",
        "pybind11"
    )
    session.install(".")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)
