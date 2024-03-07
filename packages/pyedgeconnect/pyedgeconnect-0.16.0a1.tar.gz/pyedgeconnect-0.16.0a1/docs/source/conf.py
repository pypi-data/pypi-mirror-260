# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
sys.path.insert(0, os.path.abspath("../../pyedgeconnect/orch/"))
sys.path.insert(0, os.path.abspath("../../pyedgeconnect/ecos/"))

# -- Project information ----------------------------------------------

project = "pyedgeconnect"
copyright = "2022 Hewlett Packard Enterprise Development LP"
author = "Zach Camara"

# Main version number
version = "0.16"
# The full version, including alpha/beta/rc tags
release = "0.16.0-a1"


# -- General configuration --------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output ------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation
# for a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = "_static/hpe_aruba_black_pos_rgb.png"


# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named "default.css" will overwrite the
# builtin "default.css".
html_static_path = ["_static"]


def setup(app):
    app.add_css_file("css/pyedgeconnect.css")
