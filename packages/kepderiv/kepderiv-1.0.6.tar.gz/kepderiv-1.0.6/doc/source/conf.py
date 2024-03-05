# -- Project information -----------------------------------------------------
project = 'kepderiv'
copyright = '2019-2024, Jean-Baptiste Delisle'
author = 'Jean-Baptiste Delisle'

# -- General configuration ---------------------------------------------------
needs_sphinx = '1.1'
extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.autosummary',
  'sphinx.ext.intersphinx',
  'sphinx.ext.coverage',
  'numpydoc',
]
templates_path = ['_templates']
exclude_patterns = []
pygments_style = 'sphinx'
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_theme_options = {'gitlab_url': 'https://gitlab.unige.ch/delisle/kepderiv'}
html_static_path = ['_static']
