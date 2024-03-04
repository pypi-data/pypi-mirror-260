# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

sys.path.insert(0, os.path.abspath(".."))

project = 'Documentation tscw_module'
copyright = '2024, Thomas Simader'
author = 'Thomas Simader'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'sphinx.ext.autodoc',
              'sphinx.ext.duration',
              'sphinx.ext.doctest',
              'sphinx_autodoc_typehints']
            #   'm2r2']

templates_path   = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'helper_func.py', 'process_AusEinspeisung.py']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


autodoc_default_flags = ['members', 'private-members', 'special-members',
                         #'undoc-members',
                         'show-inheritance']

def autodoc_skip_member(app, what, name, obj, skip, options):
    # Ref: https://stackoverflow.com/a/21449475/
    exclusions = ('helper_func.py')
    exclude = name in exclusions
    # return True if (skip or exclude) else None  # Can interfere with subsequent skip functions.
    return True if exclude else None
 
def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)