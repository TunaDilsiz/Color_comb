"""Render the whole site to static HTML in docs/ for GitHub Pages.

    python build.py            # links at /
    python build.py /Color_comb  # links under a repo subpath
"""
import os
import shutil
import sys
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colorsite.settings")
django.setup()

from django.test import Client
from django.test.utils import setup_test_environment
from django.urls import set_script_prefix

# the test client never sets a script prefix, so {% url %} needs it set here
set_script_prefix((sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "") + "/")
setup_test_environment()

from palette.views import COLORS

out = Path("docs")
shutil.rmtree(out, ignore_errors=True)
client = Client()
urls = ["/", "/combinations/"] + [f"/color/{c['id']}/" for c in COLORS]

for url in urls:
    page = out / url.strip("/") / "index.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_bytes(client.get(url).content)

print(f"{len(urls)} pages -> {out}/")
