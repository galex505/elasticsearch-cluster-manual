project = 'Analysis Cockpit Elasticsearch Cluster Manual'
version="1.0"
copyright = '2024, Nextron Systems GmbH'
author = 'Nextron Systems'
extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx_rtd_theme'
]
source_suffix = '.rst'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv/*']
language = "en"
master_doc = 'index'
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'prev_next_buttons_location': 'both',
    'style_external_links': True
}

html_logo = "images/html/cockpit-logo.png"
html_favicon = "images/html/favicon.ico"
html_static_path = ['_static']
html_css_files = ['css/custom.css',]
epub_title = project
epub_exclude_files = ['search.html']
intersphinx_mapping = {'https://docs.python.org/': None}
smartquotes = False
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 3
# disable epub mimetype warnings
suppress_warnings = ["epub.unknown_project_files"]