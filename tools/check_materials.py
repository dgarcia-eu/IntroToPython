#!/usr/bin/env python3
"""
Check that the course materials still work.

Run locally before teaching, and in CI on every push:

    python tools/check_materials.py            # notebooks + links, no network fetches
    python tools/check_materials.py --network  # also verify every external URL

Four checks:

1. Every lecture notebook executes top to bottom in a fresh kernel.
   A cell may raise only if it is tagged "raises-exception" - those are the
   deliberate teaching examples. An untagged exception fails the run, and so
   does a tagged cell that has stopped raising (the lesson silently died).

2. No FutureWarning or DeprecationWarning anywhere. This is what would have
   caught the pandas chained-inplace idiom (defect A4) years before pandas 3.0
   removed it.

3. Every "%load solutions/..." path in a notebook resolves to a real file.

4. With --network, every http(s) URL referenced by a notebook still answers.

Exit code 0 = clean, 1 = something needs attention.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

LECTURE_GLOB = "Day*/[0-9][0-9]_*.ipynb"
ALL_NB_GLOB = ["Day*/*.ipynb", "Day*/assignment_*/*.ipynb"]

# Warning classes that mean "this will break in a future release".
FATAL_WARNINGS = ("FutureWarning", "DeprecationWarning", "PendingDeprecationWarning")

URL_RE = re.compile(r'https?://[^\s"\'<>)\]}\\]+')
LOAD_RE = re.compile(r"^\s*#?\s*%load\s+\"?([^\"\n]+?)\"?\s*$", re.MULTILINE)


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.notes: list[str] = []

    def fail(self, msg: str) -> None:
        self.failures.append(msg)
        print(f"  FAIL  {msg}")

    def ok(self, msg: str) -> None:
        print(f"  ok    {msg}")

    def note(self, msg: str) -> None:
        self.notes.append(msg)
        print(f"  note  {msg}")


def notebooks(patterns: list[str]) -> list[str]:
    found: list[str] = []
    for pat in patterns:
        found += glob.glob(pat)
    return sorted(p for p in found if ".ipynb_checkpoints" not in p)


def splice_solutions(nb, workdir: str) -> int:
    """Replace each commented-out '%load solutions/x.py' with the file's contents.

    The solutions ship commented out so students meet the exercise first. That
    also means nothing ever executes them, so a solution can rot silently -
    exactly what happened to Exercise 3.5, which grouped by a column this
    notebook never creates. Splicing them in makes the check real.
    """
    spliced = 0
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        m = re.search(r'#\s*%load\s+"?([^"\n]+?)"?\s*$', cell.source, re.M)
        if not m:
            continue
        target = os.path.join(workdir, m.group(1).strip())
        if os.path.exists(target):
            cell.source = open(target, encoding="utf-8").read()
            spliced += 1
    return spliced


def check_execution(paths: list[str], report: Report, with_solutions: bool = False) -> None:
    print(f"\n[1/4] Executing notebooks{' with solutions spliced in' if with_solutions else ''}")
    for path in paths:
        workdir = os.path.dirname(path) or "."
        nb = nbformat.read(path, as_version=4)
        spliced = splice_solutions(nb, workdir) if with_solutions else 0
        try:
            NotebookClient(
                nb,
                timeout=600,
                kernel_name="python3",
                allow_errors=True,
                resources={"metadata": {"path": workdir}},
            ).execute()
        except CellExecutionError as exc:  # pragma: no cover - kernel level failure
            report.fail(f"{path}: kernel error: {exc}")
            continue

        unexpected, silent = [], []
        for i, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            tagged = "raises-exception" in cell.get("metadata", {}).get("tags", [])
            raised = [o for o in cell.get("outputs", []) if o.output_type == "error"]
            if raised and not tagged:
                unexpected.append(f"cell {i} ({raised[0].ename}: {raised[0].evalue[:70]})")
            elif tagged and not raised and not with_solutions:
                silent.append(f"cell {i}")

        for u in unexpected:
            report.fail(f"{path}: unexpected exception in {u}")
        for s in silent:
            report.fail(
                f"{path}: {s} is tagged raises-exception but no longer raises "
                "- the teaching example has stopped working"
            )
        if not unexpected and not silent:
            tags = sum(
                "raises-exception" in c.get("metadata", {}).get("tags", [])
                for c in nb.cells
            )
            extra = f", {spliced} solutions" if spliced else ""
            report.ok(f"{path} ({tags} deliberate exception{'s' if tags != 1 else ''}{extra})")

        check_warnings(path, nb, report)


def check_warnings(path: str, nb, report: Report) -> None:
    for i, cell in enumerate(nb.cells):
        for out in cell.get("outputs", []):
            if out.output_type != "stream" or out.get("name") != "stderr":
                continue
            for line in out.text.splitlines():
                for w in FATAL_WARNINGS:
                    if w in line:
                        report.fail(f"{path}: {w} in cell {i}: {line.strip()[:110]}")


def check_load_paths(paths: list[str], report: Report) -> None:
    print("\n[2/4] Checking %load solution paths")
    total = broken = 0
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        workdir = os.path.dirname(path) or "."
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            for target in LOAD_RE.findall("".join(cell.source)):
                total += 1
                if not os.path.exists(os.path.join(workdir, target)):
                    broken += 1
                    report.fail(f"{path}: %load target missing: {target}")
    if not broken:
        report.ok(f"all {total} %load targets resolve")


def check_urls(paths: list[str], report: Report, network: bool) -> None:
    print("\n[3/4] Checking external URLs")
    urls: dict[str, str] = {}
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        for cell in nb.cells:
            for url in URL_RE.findall("".join(cell.source)):
                urls.setdefault(url.rstrip(".,);"), path)
    if not network:
        report.note(f"{len(urls)} distinct URLs found; re-run with --network to verify them")
        return

    import urllib.error
    import urllib.request

    bad = 0
    for url, path in sorted(urls.items()):
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "IntroToPython-CI"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status >= 400:
                    bad += 1
                    report.fail(f"{url} -> HTTP {resp.status} (in {path})")
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 405):  # server dislikes HEAD, not our problem
                continue
            bad += 1
            report.fail(f"{url} -> HTTP {exc.code} (in {path})")
        except Exception as exc:
            bad += 1
            report.fail(f"{url} -> {type(exc).__name__} (in {path})")
    if not bad:
        report.ok(f"all {len(urls)} URLs reachable")


BINDER_RE = re.compile(r"mybinder\.org/v2/gh/([^/]+)/([^/]+)/([^)\s]+)")


def check_binder(report: Report, network: bool) -> None:
    """The Binder badge names a git ref. Check that ref actually has a spec.

    This is easy to get wrong and fails silently until a student clicks it. It
    already did: the badge said HEAD, which is main, but the environment lives on
    the refresh-2026 branch, so repo2docker reported "No environment specification
    found". When the branch is merged, the badge has to move back to HEAD - and
    this check is what will say so.
    """
    try:
        readme = open("README.md", encoding="utf-8").read()
    except OSError:
        return
    m = BINDER_RE.search(readme)
    if not m:
        return
    owner, repo, ref = m.groups()
    if not network:
        report.note(f"Binder badge points at {owner}/{repo}@{ref}; "
                    f"re-run with --network to check that ref has an environment file")
        return

    import urllib.error
    import urllib.request

    def exists(path: str) -> bool | None:
        """True / False, or None when GitHub would not tell us."""
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}"
        req = urllib.request.Request(url, headers={"User-Agent": "IntroToPython-CI",
                                                   "Accept": "application/vnd.github+json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.status == 200
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return False
            return None
        except Exception:
            return None

    # repo2docker's rule: if a binder/ directory exists it is the ONLY place
    # config is read from, and root-level files are ignored. Mirror that, or the
    # check passes on a root environment.yml that Binder will never look at.
    in_binder = exists("binder")
    if in_binder is None:
        report.note("Binder check skipped: could not reach the GitHub API")
        return
    candidates = (["binder/environment.yml", "binder/requirements.txt", "binder/Dockerfile"]
                  if in_binder else
                  ["environment.yml", "requirements.txt", "Dockerfile"])

    for candidate in candidates:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{candidate}?ref={ref}"
        req = urllib.request.Request(url, headers={"User-Agent": "IntroToPython-CI",
                                                   "Accept": "application/vnd.github+json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status == 200:
                    report.ok(f"Binder badge -> {ref}, which has {candidate}")
                    return
        except urllib.error.HTTPError as exc:
            if exc.code == 403:  # rate limited, not a real answer
                report.note("Binder check skipped: GitHub API rate limit")
                return
            continue
        except Exception:
            continue
    where = "binder/" if in_binder else "the repository root"
    report.fail(
        f"the Binder badge points at {owner}/{repo}@{ref}, but {where} on that ref "
        f"has none of {', '.join(candidates)}. Binder will fail with 'No environment "
        f"specification found'. Note that when a binder/ directory exists, "
        f"repo2docker ignores root-level config entirely.")


def check_kernels(paths: list[str], report: Report) -> None:
    print("\n[4/4] Checking notebook metadata")
    bad = 0
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        name = nb.metadata.get("kernelspec", {}).get("name")
        if name != "python3":
            bad += 1
            report.fail(f"{path}: kernelspec is {name!r}, expected 'python3'")
    if not bad:
        report.ok(f"all {len(paths)} notebooks declare the python3 kernel")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", action="store_true", help="also verify external URLs")
    parser.add_argument("--solutions", action="store_true",
                        help="also run every notebook with its solution files spliced in")
    args = parser.parse_args()

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

    lectures = notebooks([LECTURE_GLOB])
    every = notebooks(ALL_NB_GLOB)
    if not lectures:
        print("No notebooks found - is this the repository root?")
        return 1

    report = Report()
    check_execution(lectures, report)
    if args.solutions:
        check_execution(lectures, report, with_solutions=True)
    check_load_paths(every, report)
    check_urls(every, report, args.network)
    check_binder(report, args.network)
    check_kernels(every, report)

    print("\n" + "=" * 68)
    if report.failures:
        print(f"{len(report.failures)} problem(s) found:\n")
        for f in report.failures:
            print(f"  - {f}")
        return 1
    print(f"All checks passed: {len(lectures)} lecture notebooks, {len(every)} notebooks total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
