# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
from importlib.metadata import PackageNotFoundError, version as package_version

# -- Project information -----------------------------------------------------

project = "QCSchema"
copyright = f"2018-{datetime.datetime.today().year}, The Molecular Sciences Software Institute"
author = "Molecular Sciences Software Institute"

try:
    # The short X.Y version, and the full version including alpha/beta/rc tags
    version = release = package_version("qcschema")
except PackageNotFoundError:
    version = release = ""


# -- General configuration ---------------------------------------------------

html_title = "QCSchema documentation"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#
# The specification pages are hand-written; nothing here introspects code. The
# autodoc/autosummary extensions are enabled ready for an API reference section,
# to be added once the QCSchema v2 models live in this repository.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx_design",
    "sphinx_copybutton",
    "myst_nb",
]

# Some options
add_module_names = False
autoclass_content = "both"
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = [
    "_templates",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    ".ipynb_checkpoints/*",
    "Thumbs.db",
    ".DS_Store",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "github_url": "https://github.com/MolSSI/QCSchema",
    # Schema-version dropdown; see docs/_templates/schema-version-switcher.html
    "navbar_start": ["navbar-logo", "schema-version-switcher"],
    "logo": {
        "image_light": "qcarchive_logo.svg",
        "image_dark": "qcarchive_logo_inverted.svg",
        "text": "QCSchema",
        "molssi_light": "molssi_main_logo.png",
        "molssi_dark": "molssi_main_logo_inverted_white.png",
    },
    "show_toc_level": 2,
    "header_links_before_dropdown": 6,
    "secondary_sidebar_items": ["page-toc", "sourcelink"],
    "footer_start": ["molssi_footer"],
    "footer_end": [],
}

html_css_files = ["css/custom.css"]

html_context = {
    "extrahead": '<link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">',
    "current_year": datetime.datetime.today().year,
    # Populates the schema-version dropdown in the navbar. Both versions live in
    # this one build, so ``root`` is a docname resolved with pathto() at build
    # time. ``prefix`` is the directory a version's pages live under; the default
    # (unprefixed) version must come last, as it is the fallback.
    "schema_versions": [
        {"name": "v2", "root": "index", "note": "current", "prefix": ""},
        {"name": "v1", "root": "v1/index", "note": "legacy", "prefix": "v1"},
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- extlinks extension ------------------------------------------------------

extlinks = {
    "issue": ("https://github.com/MolSSI/QCSchema/issues/%s", "Issue %s"),
    "pr": ("https://github.com/MolSSI/QCSchema/pull/%s", "PR %s"),
    "contrib": ("https://github.com/%s", "@%s"),
}


# -- intersphinx extension ---------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

