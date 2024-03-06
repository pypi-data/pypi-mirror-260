# -*- coding: utf-8 -*-

import os

from mmpy_bot_mk2 import __version__

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.todo"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = "mmpy_bot_mk2"
copyright = "2016, "
version = __version__
release = __version__
exclude_patterns = []
pygments_style = "sphinx"
html_theme = "default"
htmlhelp_basename = "mmpy_bot_mk2_doc"
latex_documents = [
    ("index", "mmpy_bot_mk2.tex", "mmpy_bot_mk2 Documentation", "", "manual"),
]
man_pages = [("index", "mmpy_bot_mk2", "mmpy_bot_mk2 Documentation", ["gotlium"], 1)]
texinfo_documents = [
    (
        "index",
        "mmpy_bot_mk2",
        "Mattermost-bot Documentation",
        "gotlium",
        "mmpy_bot_mk2",
        "One line description of project.",
        "Miscellaneous",
    ),
]
