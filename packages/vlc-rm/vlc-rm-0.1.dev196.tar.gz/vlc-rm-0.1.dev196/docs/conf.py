# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import traceback
import python_docs_theme

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'vlc-rm'
year = '2022'
author = 'Juan F. Gutierrez'
copyright = '{0}, {1}'.format(year, author)
try:
    from pkg_resources import get_distribution

    version = release = get_distribution('vlc_rm').version
except Exception:
    traceback.print_exc()
    version = release = '0.0.0'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/jufgutierrezgo/python-vlc-rm/issues/%s', '#'),
    'pr': ('https://github.com/jufgutierrezgo/python-vlc-rm/pull/%s', 'PR #'),
}
html_theme = 'python_docs_theme'
html_theme_path = [python_docs_theme.get_html_theme_path()]
html_theme_options = {
    'githuburl': 'https://github.com/jufgutierrezgo/python-vlc-rm/',
}

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
    '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
