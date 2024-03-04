"""Standard integration tests."""

import shutil
from io import StringIO
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test__it(app: SphinxTestApp, status: StringIO, warning: StringIO):
    """Test to pass."""


@pytest.mark.parametrize("theme", ["alabaster", "haiku", "furo", "sphinx_rtd_theme"])
def test__work_on_theme(
    sphinx_test_tempdir: Path, rootdir: Path, make_app: callable, theme: str
):
    testroot = "root"
    srcdir = sphinx_test_tempdir / testroot
    if not srcdir.exists():
        testroot_path = rootdir / f"test-{testroot}"
        shutil.copytree(testroot_path, srcdir)

    app: SphinxTestApp = make_app(
        "html", srcdir=srcdir, confoverrides={"html_theme": theme}
    )
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "html.parser")
    assert "hx-boost" in soup.body.attrs
