#!/usr/bin/env python3
"""
Generate the daily feedback redirect pages and their QR codes.

    python tools/make_feedback.py            # regenerate everything
    python tools/make_feedback.py --check    # verify, change nothing (CI)

Why this exists
---------------
Making a new form and a new QR code for every day of every year is four
images and four slide edits a year, done in the week when there is least
time to do them. The fix is to stop pointing the QR code at the survey.

Each QR code encodes a permanent address in this repository:

    https://dgarcia-eu.github.io/IntroToPython/feedback-form/day1/

That address serves a two-line HTML page which forwards to whichever survey
is collecting answers this year. So:

  * the QR images are generated once and stay correct forever, and the
    slides never need touching again;
  * opening next year's forms is editing "target" in feedback-form/forms.toml
    and running this script;
  * if the survey platform ever has to change, nothing that a student has
    already scanned or bookmarked breaks.

The survey itself is deliberately not this script's business. Anything with
a stable URL works: a SoSci Survey project on the university server, an
ILIAS survey, EUSurvey, a self-hosted instance.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import tomllib

try:
    import segno
except ImportError:  # pragma: no cover
    segno = None

CONFIG = "feedback-form/forms.toml"
MANIFEST = "feedback-form/MANIFEST.txt"

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
{refresh}<title>Day {day} feedback</title>
<style>
  body {{ margin: 0; padding: 2.5rem 1.25rem; font-family: system-ui, sans-serif;
         line-height: 1.5; color: #222; background: #fff; }}
  main {{ max-width: 32rem; margin: 0 auto; }}
  h1 {{ font-size: 1.5rem; margin: 0 0 .25rem 0; }}
  p.course {{ margin: 0 0 2rem 0; color: #666; }}
  a.go {{ display: inline-block; padding: .75rem 1.5rem; background: #123;
         color: #fff; text-decoration: none; border-radius: .4rem;
         font-size: 1.1rem; }}
  p.note {{ margin-top: 2rem; font-size: .9rem; color: #666; }}
</style>
</head>
<body>
<main>
<h1>Feedback on Day {day}</h1>
<p class="course">{course} &middot; {year}</p>
{body}{privacy}
</main>
</body>
</html>
"""

FORWARD_BODY = """<p>Taking you to the form. If nothing happens:</p>
<p><a class="go" href="{target}">Open the feedback form</a></p>"""

HOLDING_BODY = """<p><strong>This form is not open yet.</strong></p>
<p>It opens on the morning after Day {day} of the course. Please try the
QR code again then, or ask in the session.</p>"""


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def render(cfg: dict, form: dict) -> str:
    target = form.get("target", "").strip()
    if target:
        refresh = f'<meta http-equiv="refresh" content="0; url={esc(target)}">\n'
        body = FORWARD_BODY.format(target=esc(target))
        # The privacy line describes the destination, so it only belongs on a
        # page that has one. Saying where answers are stored when no survey is
        # configured would be a claim about nothing.
        privacy = f'\n<p class="note">{esc(cfg["privacy"])}</p>'
    else:
        refresh = ""
        body = HOLDING_BODY.format(day=form["day"])
        privacy = ""
    return PAGE.format(
        refresh=refresh,
        day=form["day"],
        course=esc(cfg["course"]),
        year=cfg["year"],
        privacy=privacy,
        body=body,
    )


def permanent_url(cfg: dict, form: dict) -> str:
    return f"{cfg['base_url'].rstrip('/')}/day{form['day']}/"


def qr_png(url: str) -> bytes:
    if segno is None:
        sys.exit("segno is not installed. Run: pip install segno")
    import io
    buf = io.BytesIO()
    # Error correction M: the usual choice for a projected slide. The QR now
    # fills most of the slide height (see .qr-code in assets/introtopython.scss),
    # so scale 20 gives roughly 740px, comfortably above what a 720p slide
    # displays. Rendering above the displayed size, rather than below it, is
    # what keeps the module edges hard on a projector.
    segno.make(url, error="m").save(buf, kind="png", scale=20, border=2)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="verify the committed files match the config; write nothing")
    args = ap.parse_args()

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    with open(CONFIG, "rb") as fh:
        cfg = tomllib.load(fh)

    problems: list[str] = []
    manifest: list[str] = []
    open_forms = 0

    for form in cfg["form"]:
        day, deck = form["day"], form["deck"]
        url = permanent_url(cfg, form)
        page_path = f"feedback-form/day{day}/index.html"
        png_path = f"{deck}/Slides/QR.png"
        html = render(cfg, form)
        if form.get("target", "").strip():
            open_forms += 1

        if args.check:
            # Note what the config says this QR code must encode, but do NOT
            # re-encode it: a segno upgrade could change the PNG bytes without
            # changing what the code means, and that must not turn CI red.
            # The hash comparison below is against the committed manifest, so
            # the failure this really catches is the one that matters: a config
            # edited without rerunning this script.
            manifest.append(f"day{day}\t{url}\t{png_path}")
            if not os.path.exists(page_path):
                problems.append(f"{page_path} is missing; run tools/make_feedback.py")
            elif open(page_path, encoding="utf-8").read() != html:
                problems.append(f"{page_path} is out of date; run tools/make_feedback.py")
            if not os.path.exists(png_path):
                problems.append(f"{png_path} is missing; run tools/make_feedback.py")
        else:
            png = qr_png(url)
            manifest.append(f"day{day}\t{url}\t{png_path}\t{hashlib.sha256(png).hexdigest()}")
            os.makedirs(os.path.dirname(page_path), exist_ok=True)
            with open(page_path, "w", encoding="utf-8") as fh:
                fh.write(html)
            with open(png_path, "wb") as fh:
                fh.write(png)
            print(f"  day {day}  {url}  ->  {form.get('target') or '(not open yet)'}")
            print(f"           {page_path}, {png_path}")

    if args.check:
        recorded = [l for l in open(MANIFEST, encoding="utf-8").read().splitlines() if l] \
                   if os.path.exists(MANIFEST) else []
        if [l.rsplit("\t", 1)[0] for l in recorded] != manifest:
            problems.append(f"{MANIFEST} does not list what {CONFIG} describes; "
                            f"run tools/make_feedback.py")
        else:
            for line in recorded:
                _, _, png_path, digest = line.split("\t")
                actual = hashlib.sha256(open(png_path, "rb").read()).hexdigest()
                if actual != digest:
                    problems.append(
                        f"{png_path} is not the QR code recorded in {MANIFEST}. "
                        f"Either it was edited by hand, or the config changed "
                        f"without rerunning tools/make_feedback.py")
        if problems:
            print(f"{len(problems)} problem(s):\n")
            for p in problems:
                print(f"  - {p}")
            return 1
        print(f"Feedback forms OK: {len(cfg['form'])} permanent QR codes, "
              f"{open_forms} form(s) currently open.")
        return 0

    with open(MANIFEST, "w", encoding="utf-8") as fh:
        fh.write("\n".join(manifest) + "\n")
    print(f"\nWrote {len(cfg['form'])} redirect pages and QR codes, "
          f"{open_forms} form(s) currently open.")
    if open_forms < len(cfg["form"]):
        print("Set 'target' for each form in feedback-form/forms.toml to open them.\n"
              "The QR codes above are already final and do not change when you do.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
