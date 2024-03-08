"""Sphinx configuration."""
from datetime import datetime

project = "qamlib"
author = "Daniel Lundberg Pedersen"
copyright = f"{datetime.now().year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosummary",
    "breathe",
]

autodoc_typehints = "description"
autodoc_member_order = "groupwise"
autodoc_default_options = {
    "members": None, # This shows all members
    "undoc-members": True,
}

breathe_projects = {"qamlib": "doxygen/xml/"}
breathe_default_project = "qamlib"
breathe_default_members = (
    "members", # This shows all members
    "undoc-members",
)


html_theme = "furo"
todo_include_todos = True

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
exclude_patterns = ["_build", "_templates"]
