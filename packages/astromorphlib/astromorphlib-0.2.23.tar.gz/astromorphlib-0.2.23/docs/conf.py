# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'astromorphlib'
copyright = '2023, Jose Hernandez-Jimenez & Angela Krabbe'
author = 'Jose Hernandez-Jimenez & Angela Krabbe'
release = '0.2.18'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [ 'sphinx.ext.autodoc', 
 'sphinx.ext.imgmath', 
 'sphinx.ext.viewcode',
 'sphinx.ext.napoleon',
 'sphinx.ext.mathjax', 
 'nbsphinx',           
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'classic'
html_static_path = ['_static']
html_logo = "_static/logo.png"
html_theme_options = {
   'globaltoc_maxdepth':"2", 
}
