#!/usr/bin/env python3
"""
Recompute the "Session plan" estimate at the top of each lecture notebook.

The budgets were written once, by hand, and then went stale as scaffolding was
added to the notebooks: Parsons problems, faded examples, framing cells, the
debugging session, comparison tables, the closing blocks. 41_modules_exceptions
ended up claiming 15 minutes for 35 minutes of material. A budget that
understates the content is worse than none, because the whole point of it is to
decide what to cut before the session rather than during it.

Run this after adding or removing notebook content:

    python tools/update_session_budgets.py            # report only
    python tools/update_session_budgets.py --write     # rewrite the cells

Estimates come from content volume at CHARS_PER_MIN, calibrated against the
2025 timings. They under-weight pandas and visualisation, where cells are short
but each produces output worth discussing, so treat them as a starting point to
calibrate against the room rather than as measurements.

The morning is 9:30-13:00 with one short break, so MORNING_MINUTES is 200 and
a day is flagged only above that.

"Core" excludes every section whose heading carries [IF TIME] or
[EXTRA - read at home], from that heading up to the next heading.
"""
from __future__ import annotations

import glob
import json
import re
import sys

CHARS_PER_MIN = 260

# 9:30-13:00 with one short break in the middle.
MORNING_MINUTES = 200

# Not taught sessions: the Day 0 self-check, and the redirect stub left behind
# at the old Day 2 filename.
# The Day 0 self-check is not a taught session, so it carries no session plan.
SKIP_FILES = {"Day1/00_day0_selfcheck.ipynb"}

HEADING = re.compile(r"^#{1,4} ", re.M)

# Only the numbers are ever touched. The wording of the session plan cell is
# David's, and the first notebook of each day carries a longer version that
# explains the [IF TIME] and [EXTRA] labels, so rewriting the whole cell from a
# template here would flatten both. Matching the "approx N min" occurrences in
# place leaves everything else exactly as written.
MINUTES_IN_PLAN = re.compile(r"(\u2248 \*\*)(\d+)( min\*\*)")

def minutes(chars: int) -> int:
    return max(5, round(chars / CHARS_PER_MIN / 5) * 5)


def measure(cells) -> tuple[int, int]:
    """(core chars, total chars)."""
    total = skippable = 0
    in_skip = False
    for c in cells:
        s = "".join(c["source"])
        total += len(s)
        if c["cell_type"] == "markdown" and HEADING.search(s):
            # The marker only counts when it is on the heading LINE. The closing
            # "Where we got to" block mentions [IF TIME] in its prose, and
            # matching anywhere in the cell made that block look skippable.
            head = HEADING.search(s)
            line = s[head.start():].split("\n", 1)[0]
            in_skip = "[IF TIME]" in line or "[EXTRA" in line
        if in_skip:
            skippable += len(s)
    return total - skippable, total


def main() -> int:
    write = "--write" in sys.argv
    changed = 0
    per_day: dict[str, list[int]] = {}
    for path in sorted(glob.glob("Day*/[0-9][0-9]_*.ipynb")):
        if path in SKIP_FILES:
            continue
        nb = json.load(open(path, encoding="utf-8"))
        cells = nb["cells"]
        core, total = measure(cells)
        c_min, t_min = minutes(core), minutes(total)
        day = path.split("/")[0]
        per_day.setdefault(day, [0, 0])
        per_day[day][0] += core
        per_day[day][1] += total

        idx = next((i for i, c in enumerate(cells[:8])
                    if "**Session plan**" in "".join(c["source"])
                    or "**Session plan:**" in "".join(c["source"])), None)
        if idx is None:
            print(f"  {path}: no session plan cell")
            continue
        src = "".join(cells[idx]["source"])
        found = MINUTES_IN_PLAN.findall(src)
        if not found:
            print(f"  {path}: session plan cell has no minute figure to update")
            continue

        # One figure means an all-core notebook; two means core then everything.
        wanted = [t_min] if len(found) == 1 else [c_min, t_min]
        if len(found) != len(wanted):
            print(f"  {path}: expected {len(wanted)} minute figures, found {len(found)}")
            continue
        if [int(f[1]) for f in found] == wanted:
            print(f"  {path}: already {'/'.join(str(w) for w in wanted)} min")
            continue

        it = iter(wanted)
        new = MINUTES_IN_PLAN.sub(lambda m: f"{m.group(1)}{next(it)}{m.group(3)}", src)
        print(f"  {path}: {'/'.join(f[1] for f in found)} -> "
              f"{'/'.join(str(w) for w in wanted)} min")
        changed += 1
        if write:
            cells[idx]["source"] = new.splitlines(keepends=True)
            json.dump(nb, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            open(path, "a", encoding="utf-8").write("\n")

    print()
    for day, (c, t) in sorted(per_day.items()):
        # The morning runs 9:30-13:00 with one short break, so about 200 minutes
        # of teaching time.
        flag = "  <-- over the 200 min morning" if minutes(c) > MORNING_MINUTES else ""
        print(f"  {day}: core {minutes(c)} min, everything {minutes(t)} min{flag}")
    print()
    print(f"{changed} notebook(s) {'updated' if write else 'would change'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
