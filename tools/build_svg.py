"""Build the downloadable SVG launcher from the canonical game page."""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def build_svg():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    template = (ROOT / "tools/index.svg.in").read_text(encoding="utf-8")
    # Split literal CDATA terminators without changing the embedded HTML.
    svg = template.replace("@@INDEX_HTML@@", html.replace("]]>", "]]]]><![CDATA[>"))
    source = ET.fromstring(svg).find("{http://www.w3.org/2000/svg}metadata")
    if source is None or source.text != html:
        raise ValueError("SVG does not contain the complete index.html")
    return svg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check without writing the SVG")
    args = parser.parse_args()
    output = ROOT / "index.svg"
    generated = build_svg()
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != generated:
            parser.exit(1, "index.svg is stale. Run python3 tools/build_svg.py\n")
    else:
        output.write_text(generated, encoding="utf-8")
