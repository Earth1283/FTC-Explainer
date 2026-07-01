# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FTC-Explainer'
copyright = '2026, 32008'
author = 'Earth1283'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxcontrib.mermaid',
    'sphinx.ext.mathjax',
    'sphinx.ext.autosectionlabel',
    'sphinx_copybutton',
    'sphinx_design',
]

# Prefix section labels with the document name so identical headings in
# different pages (e.g. "Overview") don't collide when cross-referenced.
autosectionlabel_prefix_document = True

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# Copy buttons: skip the '$ ' shell prompt and '>>> ' REPL prompt so users
# copy only runnable text.
copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
