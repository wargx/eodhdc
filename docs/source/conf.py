# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import tomli
from datetime import datetime

sys.path.insert(0, os.path.abspath("../.."))


with open("../../pyproject.toml", mode="rb") as pyproject:
    meta = tomli.load(pyproject)["tool"]["poetry"]


project = meta["name"]
copyright = f"{datetime.now().year}, Warg"
author = meta["authors"][0]
version = meta["version"]
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

extensions.append("sphinx.ext.autodoc")
extensions.append("myst_parser")

suppress_warnings = ["myst.header"]
myst_enable_extensions = ["tasklist"]
myst_enable_checkboxes = True
