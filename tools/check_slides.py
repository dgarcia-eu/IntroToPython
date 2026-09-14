#!/usr/bin/env python3
"""
Render the slide decks and check nothing falls off a 1280x720 (16:9) slide.

    python tools/check_slides.py            # all decks
    python tools/check_slides.py Day3       # one deck

Each deck is rendered, printed to PDF through headless Chrome (which is what
reveal.js's ?print-pdf mode is for: one page per slide, at the deck's real
aspect ratio), then every page is inspected pixel by pixel. Ink touching the
left, right or bottom edge means content is being cut off on screen.

Adapted from ICSS-local/ICSS_2026/tools/build.sh, which does the same job for
the ICSS decks.
"""
from __future__ import annotations

import glob
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = next((c for c in ("google-chrome", "chromium", "chromium-browser")
               if subprocess.run(["which", c], capture_output=True).returncode == 0), None)


def scan(pdf: str, workdir: str) -> tuple[int, list[str]]:
    from PIL import Image
    subprocess.run(["pdftoppm", "-png", "-r", "72", pdf, os.path.join(workdir, "p")], check=True)
    pages = sorted(glob.glob(os.path.join(workdir, "p-*.png")))
    bad = []
    for f in pages:
        im = Image.open(f).convert("L")
        w, h = im.size
        floor = int(h * 0.945)          # above the footer bar
        left = any(im.getpixel((1, y)) < 245 for y in range(60, floor))
        right = any(im.getpixel((w - 2, y)) < 245 for y in range(60, floor))
        bottom = any(im.getpixel((x, floor - 2)) < 245 for x in range(5, w - 5))
        if left or right or bottom:
            edges = "".join(e for e, hit in (("left", left), ("right", right), ("bottom", bottom)) if hit)
            bad.append(f"{os.path.basename(f)}: {', '.join(e for e, hit in (('left', left), ('right', right), ('bottom', bottom)) if hit)}")
    return len(pages), bad


def slide_titles(qmd: str) -> list[str]:
    """The '## ' headings in the source, cleaned of markdown emphasis."""
    out = []
    for line in open(qmd, encoding="utf-8").read().split("\n"):
        if line.startswith("## "):
            t = line[3:].strip().strip("*").replace("**", "").replace("*", "")
            out.append(" ".join(t.split()))
    return out


def check_nothing_lost(qmd: str, pdf: str) -> list[str]:
    """Every slide heading in the source must appear in the printed deck.

    Overflow makes content invisible on screen but still present in the PDF, so
    this is a separate question from the pixel scan: it catches a slide that
    silently failed to render at all.
    """
    text = subprocess.run(["pdftotext", pdf, "-"], capture_output=True,
                          text=True).stdout

    def normalise(x: str) -> str:
        # Quarto turns straight quotes and hyphens into typographic ones, so
        # compare on a flattened form or every quoted title is a false alarm.
        for a, b in (("\u201c", '"'), ("\u201d", '"'), ("\u2018", "'"),
                     ("\u2019", "'"), ("\u2013", "-"), ("\u2014", "-"),
                     ("&ndash;", "-"), ("&mdash;", "-")):
            x = x.replace(a, b)
        return " ".join(x.split()).lower()

    flat = normalise(text)
    missing = []
    for t in slide_titles(qmd):
        probe = normalise(t).split("(")[0].strip()[:40]
        if probe and probe not in flat:
            missing.append(t)
    return missing


def main() -> int:
    missing = [t for t in ("quarto", "pdftoppm")
               if subprocess.run(["which", t], capture_output=True).returncode != 0]
    if CHROME is None:
        missing.append("google-chrome or chromium")
    if missing:
        print("Cannot check slides: " + ", ".join(missing) + " not installed.")
        print("Needed: quarto (render), Chrome (print to PDF), poppler-utils (pdftoppm).")
        return 1
    only = sys.argv[1] if len(sys.argv) > 1 else None
    decks = sorted(glob.glob(os.path.join(ROOT, "Day*/Slides/Day*.qmd")))
    if only:
        decks = [d for d in decks if only in d]
    problems = 0
    for qmd in decks:
        name = os.path.basename(qmd)[:-4]
        d = os.path.dirname(qmd)
        subprocess.run(["quarto", "render", qmd, "--quiet"], check=True,
                       capture_output=True)
        html = os.path.join(d, name + ".html")
        with tempfile.TemporaryDirectory() as tmp:
            pdf = os.path.join(tmp, "deck.pdf")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                            "--virtual-time-budget=40000",
                            "--run-all-compositor-stages-before-draw",
                            "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                            f"file://{html}?print-pdf"],
                           capture_output=True, timeout=180)
            if not os.path.exists(pdf):
                print(f"{name}: FAILED to print to PDF")
                problems += 1
                continue
            n, bad = scan(pdf, tmp)
            missing = check_nothing_lost(qmd, pdf)
        if missing:
            problems += len(missing)
            print(f"{name}: MISSING from the rendered deck: {'; '.join(missing)}")
        if bad:
            problems += len(bad)
            print(f"{name}: {n} slides, {len(bad)} OVERFLOWING")
            for b in bad:
                print(f"    {b}")
        elif not missing:
            print(f"{name}: {n} pages, {len(slide_titles(qmd))} slide headings, all present and all fit")
    print()
    print("All slides fit in 16:9." if not problems else f"{problems} slide(s) need attention.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
