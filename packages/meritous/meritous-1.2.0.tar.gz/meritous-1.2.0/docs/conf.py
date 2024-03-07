import os
import sys
sys.path.insert(0, os.path.abspath('../source'))

project = 'Meritous - Simple Python Models'
copyright = '2023, Tom Morton'
author = 'Tom Morton'
release = '1.0.2'

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon"
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
