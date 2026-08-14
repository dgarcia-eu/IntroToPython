#!/usr/bin/env python3
"""
Refuse to let student data into the public repository.

This repository is public. Grading sheets, feedback exports, exam papers and
assignment answer keys live in IntroToPython_private and must never appear
here. This script fails the build if anything of that shape shows up.

    python tools/check_no_personal_data.py

It checks tracked files only, so it sees exactly what a push would publish.
Run it before committing, and let CI run it on every push.
"""
from __future__ import annotations

import re
import subprocess
import sys

# --- what must never be committed here ---------------------------------------

FORBIDDEN_PATHS = [
    (re.compile(r"grading", re.I), "grading sheets contain student names and Matrikelnummern"),
    (re.compile(r"(^|/)feedback/", re.I), "student feedback exports are personal data"),
    (re.compile(r"matrikel", re.I), "Matrikelnummern are personal data"),
    (re.compile(r"klausur|noten|grades?[-_.]", re.I), "assessment records are personal data"),
    (re.compile(r"finalexam|final[-_]exam|exam[-_]?(paper|20\d\d)", re.I), "exam papers belong in the private repository"),
    (re.compile(r"assignment[^/]*solution", re.I), "assignment answer keys belong in the private repository"),
    (re.compile(r"\.(xlsx|xls|docx|doc)$", re.I), "office documents are how grade lists travel; keep them private"),
    (re.compile(r"tutor[-_]?(guide|hints?)", re.I), "tutor guides and hint sheets belong in the private repository"),
    (re.compile(r"coverage_matrix", re.I), "the coverage matrix reveals task-by-task solution structure"),
]

# Emails that are meant to be here. Anything else is treated as a leak.
ALLOWED_EMAILS = {
    # The instructor's own institutional address, on the slides and in the README.
    "david.garcia@uni-konstanz.de",
    # Author attribution inside the jQuery "Sticky Tabs" plugin that Pandoc embeds
    # in generated HTML (README.html, setup/Anaconda.html). A third-party library
    # licence header, not anyone's personal data.
    "aidan@php.net",
}

# Vocabulary that only shows up in student records.
FORBIDDEN_WORDS = re.compile(
    r"\b(matrikelnummer|matrikel-nr|studiengang|pr[uü]fungsnummer|"
    r"nachname\s*,\s*vorname|student\s+id\s*[:=])", re.I)

TEXTUAL = re.compile(r"\.(ipynb|md|py|txt|csv|json|qmd|yml|yaml|html)$", re.I)
SKIP = re.compile(r"(_files/|_extensions/|\.min\.|/libs/)")

EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if p]


def main() -> int:
    problems: list[str] = []
    files = tracked()

    for path in files:
        for pattern, why in FORBIDDEN_PATHS:
            if pattern.search(path):
                problems.append(f"{path}\n      {why}")

    scanned = 0
    for path in files:
        if not TEXTUAL.search(path) or SKIP.search(path):
            continue
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        scanned += 1
        for addr in set(EMAIL.findall(text)):
            if addr.lower() not in ALLOWED_EMAILS and not addr.endswith((".png", ".jpg", ".svg", ".gif")):
                problems.append(f"{path}\n      contains the email address {addr!r}, "
                                f"which is not on the allowlist in this script")
        found = FORBIDDEN_WORDS.search(text)
        if found:
            line = text[:found.start()].count("\n") + 1
            problems.append(f"{path}:{line}\n      contains {found.group(0)!r}, "
                            f"which only appears in student records")

    print(f"Checked {len(files)} tracked files ({scanned} scanned for content).")
    if problems:
        print(f"\nThis repository is PUBLIC. {len(problems)} problem(s) must be fixed "
              f"before pushing:\n")
        for p in problems:
            print(f"  - {p}")
        print("\nIf a file genuinely belongs here, add it to the allowlists at the top "
              "of tools/check_no_personal_data.py, with a comment saying why.")
        return 1

    print("No student data found. Safe to publish.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
