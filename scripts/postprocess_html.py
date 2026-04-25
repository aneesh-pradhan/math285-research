#!/usr/bin/env python3
"""Post-process TeX4ht output for GitHub Pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TITLE = "Exploring the Use of Differential Equations in Electric Circuits"

MATHJAX_CONFIG = r"""<script>
window.MathJax = {
  tex: {
    tags: "ams",
    macros: {
      vC: "v_C",
      Vs: "V_s",
      Rcrit: "R_{\\\\mathrm{crit}}"
    }
  }
};
</script>"""

PDF_BAR = """<div class="site-actions">
  <a href="main.pdf">View PDF</a>
  <a href="#x1-2r1">Read HTML</a>
</div>"""


def remove_unreferenced_tex4ht_svgs(html_path: Path, html: str) -> None:
    used_assets = set(re.findall(r"""src=['"]([^'"]+)['"]""", html))
    for svg_path in html_path.parent.glob("index*x.svg"):
        if svg_path.name not in used_assets:
            svg_path.unlink()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: postprocess_html.py docs/index.html", file=sys.stderr)
        return 2

    html_path = Path(sys.argv[1])
    html = html_path.read_text(encoding="utf-8")

    html = html.replace("<head><title></title>", f"<head><title>{TITLE}</title>")

    html = re.sub(
        r"<script>\s*window\.MathJax = \{.*?\};\s*</script>",
        MATHJAX_CONFIG,
        html,
        count=1,
        flags=re.DOTALL,
    )

    if "site.css" not in html:
        html = html.replace(
            "<link href='index.css' rel='stylesheet' type='text/css' />",
            "<link href='index.css' rel='stylesheet' type='text/css' />\n"
            "<link href='site.css' rel='stylesheet' type='text/css' />",
            1,
        )

    if 'class="site-actions"' not in html:
        html = html.replace("<body>", f"<body>\n{PDF_BAR}", 1)

    html_path.write_text(html, encoding="utf-8")
    remove_unreferenced_tex4ht_svgs(html_path, html)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
