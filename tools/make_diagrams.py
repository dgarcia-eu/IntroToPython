#!/usr/bin/env python3
"""
Draw the explanatory diagrams used in the lecture notebooks.

    python tools/make_diagrams.py

Writes PNGs into Day2/img/ and Day3/img/. Run it after changing anything
here and commit both this file and the images.

Why PNG and not SVG. The notebooks have to render in Jupyter *and* on
github.com, and GitHub sanitises notebook HTML; SVG is the format that
sanitisers block. Day5/img/ already proves relative PNG works in this
repository, so these follow that pattern.

Why a script and not hand-drawn files. Four diagrams only teach if they
share one vocabulary, and a generator is the only way to keep that true
after the fifth one is added. The vocabulary is:

    a NAME    is a plain label
    a VALUE   is a filled box
    an ARROW  means "refers to" or "hands back"

Deliberately no flowchart notation: no decision diamonds, no start/stop
nodes, nothing a student has to be taught how to read first.
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# Colourblind-safe and distinguishable in greyscale print.
BLUE, ORANGE, PURPLE = "#2c7fb8", "#d95f0e", "#6a51a3"
FILL, EDGE, INK, MUTED = "#dceefb", "#1f4e79", "#1a1a1a", "#666666"
MONO = {"family": "DejaVu Sans Mono"}
SANS = {"family": "DejaVu Sans"}
DPI = 200


def canvas(w, h):
    # The figure is created at the dpi it will be saved at, and drawn once, so
    # that text measured with text_width() is measured under exactly the same
    # conditions it is rendered under. Measuring at 100 dpi and saving at 200
    # made every run of code slightly wider than its measurement, which showed
    # up as the next span overlapping the previous one by about a character.
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.canvas.draw()
    return fig, ax


def box(ax, x, y, w, h, text, fill=FILL, edge=EDGE, size=13, mono=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08",
                                linewidth=1.6, facecolor=fill, edgecolor=edge))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=INK,
            fontsize=size, **(MONO if mono else SANS))


def name(ax, x, y, text, size=15):
    ax.text(x, y, text, ha="right", va="center", color=INK, fontsize=size,
            fontweight="bold", **MONO)


def arrow(ax, p, q, color=EDGE, lw=1.8, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=16,
                                 linewidth=lw, color=color,
                                 shrinkA=2, shrinkB=2))


def note(ax, x, y, text, size=11, color=MUTED, ha="center", mono=False, bold=False):
    ax.text(x, y, text, ha=ha, va="center", color=color, fontsize=size,
            fontweight="bold" if bold else "normal", **(MONO if mono else SANS))


def save(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.12,
                facecolor="white")
    plt.close(fig)
    print(f"  wrote {path}")


def text_width(ax, t):
    """Width of a drawn text object in data units.

    The first version of the comprehension diagram assumed a fixed monospace
    character width. It was wrong by enough that the highlight bands did not
    line up with their own text and the colons floated away from the code.
    Measuring is the only way to place a band behind a run of text.
    """
    fig = ax.get_figure()
    bb = t.get_window_extent(fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x0, _), (x1, _) = inv.transform((bb.x0, bb.y0)), inv.transform((bb.x1, bb.y1))
    return x1 - x0


def code_run(ax, x, y, parts, size=14, gap=0.07):
    """Draw code left to right. parts is [(text, colour or None)].

    A coloured part gets a tinted band behind it. The pairing between the two
    code blocks is carried by colour alone: an earlier version drew connecting
    arrows, which crossed each other into spaghetti because the first part of a
    comprehension is the last line of the loop, and a version after that put
    numbered badges above each band, which crowded the line above it. The
    colours say it without either.
    """
    for text, colour in parts:
        t = ax.text(x, y, text, ha="left", va="center", fontsize=size,
                    color=colour or INK, zorder=3,
                    fontweight="bold" if colour else "normal", **MONO)
        w = text_width(ax, t)
        if colour:
            ax.add_patch(FancyBboxPatch((x - 0.05, y - 0.27), w + 0.10, 0.54,
                                        boxstyle="round,pad=0.01,rounding_size=0.06",
                                        linewidth=0, facecolor=colour, alpha=0.16,
                                        zorder=2))
            w += gap          # so a following ":" clears the tint
        x += w
    return x


def tint(hex_colour, amount=0.22):
    """Blend a colour toward white, for a fill that text still reads on."""
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(c + (255 - c) * (1 - amount)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def grid(ax, x, y, rows, col_w, row_h=0.62, size=11, header=True,
         row_fills=None, edge=EDGE):
    """A small table. rows[0] is the header when header is True.

    row_fills, if given, is one colour (or None) per body row, so a diagram can
    tint the rows a filter keeps.
    """
    top = y
    for r, cells in enumerate(rows):
        yy = top - r * row_h
        for c, text in enumerate(cells):
            w = col_w[c] if isinstance(col_w, (list, tuple)) else col_w
            xx = x + (sum(col_w[:c]) if isinstance(col_w, (list, tuple)) else c * col_w)
            if header and r == 0:
                fill, bold = FILL, True
            else:
                raw = row_fills[r - 1] if row_fills else None
                fill = tint(raw) if raw else "#ffffff"
                bold = False
            ax.add_patch(FancyBboxPatch((xx, yy - row_h), w, row_h,
                                        boxstyle="square,pad=0", linewidth=1.1,
                                        facecolor=fill, edgecolor=edge, zorder=2))
            ax.text(xx + w / 2, yy - row_h / 2, text, ha="center", va="center",
                    color=INK, fontsize=size, zorder=3,
                    fontweight="bold" if bold else "normal", **MONO)
    total_w = sum(col_w) if isinstance(col_w, (list, tuple)) else len(rows[0]) * col_w
    return total_w, len(rows) * row_h


# --------------------------------------------------------------------------
def two_names_one_list(path):
    """Diagram 1: b = a versus b = [1, 2, 3]."""
    fig, ax = canvas(11, 4.3)

    ax.plot([5.5, 5.5], [0.45, 3.75], color="#cccccc", lw=1.2, ls=(0, (4, 4)))

    # Left: one list, two names.
    note(ax, 2.6, 3.9, "b = a", size=14, color=INK, bold=True, mono=True)
    name(ax, 0.75, 2.75, "a")
    name(ax, 0.75, 1.55, "b")
    box(ax, 2.6, 1.75, 2.2, 0.85, "[1, 2, 3]")
    arrow(ax, (0.95, 2.75), (2.55, 2.35))
    arrow(ax, (0.95, 1.55), (2.55, 1.95))
    note(ax, 2.6, 1.1, "one list, two names", size=11)
    note(ax, 2.6, 0.62, "a is b  →  True", size=12, color=BLUE, mono=True)

    # Right: two lists that look alike.
    note(ax, 8.4, 3.9, "b = [1, 2, 3]", size=14, color=INK, bold=True, mono=True)
    name(ax, 6.65, 2.85, "a")
    name(ax, 6.65, 1.5, "b")
    box(ax, 7.4, 2.45, 2.2, 0.8, "[1, 2, 3]")
    box(ax, 7.4, 1.1, 2.2, 0.8, "[1, 2, 3]")
    arrow(ax, (6.85, 2.85), (7.35, 2.85))
    arrow(ax, (6.85, 1.5), (7.35, 1.5))
    note(ax, 8.5, 0.62, "a is b  →  False", size=12, color=ORANGE, mono=True)

    note(ax, 5.5, 0.12,
         "a == b is True on both sides: equality asks what the values are, "
         "identity asks whether it is the same object.",
         size=11.5, color=INK)
    save(fig, path)


# --------------------------------------------------------------------------
def slicing(path):
    """Diagram 2: slice numbers are the cuts, not the items."""
    items = ["bernice", "cody", "aaron", "ever", "dalia"]
    w, gap, x0, ybox, hbox = 1.85, 0.0, 0.85, 2.0, 0.85
    fig, ax = canvas(x0 * 2 + len(items) * w, 4.6)

    for i, it in enumerate(items):
        box(ax, x0 + i * (w + gap), ybox, w, hbox, f"'{it}'", size=11.5)
        note(ax, x0 + i * (w + gap) + w / 2, ybox - 0.42, str(i), size=13, color=INK)
        note(ax, x0 + i * (w + gap) + w / 2, ybox - 0.92, str(i - len(items)),
             size=12, color=MUTED)

    # Cut positions sit on the box edges, not under the boxes.
    for k in range(len(items) + 1):
        x = x0 + k * (w + gap)
        ax.plot([x, x], [ybox + hbox + 0.06, ybox + hbox + 0.42],
                color=ORANGE, lw=1.6)
        note(ax, x, ybox + hbox + 0.62, str(k), size=12.5, color=ORANGE)

    a, b = 1, 4
    xa, xb = x0 + a * (w + gap), x0 + b * (w + gap)
    ax.add_patch(FancyBboxPatch((xa, ybox - 0.06), xb - xa, hbox + 0.12,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                linewidth=2.4, facecolor="none", edgecolor=ORANGE))
    note(ax, (xa + xb) / 2, ybox + hbox + 1.18, "usernames[1:4]", size=14,
         color=ORANGE, bold=True, mono=True)

    # All three row labels end at the same x, clear of the first number. The
    # "cut" label used to sit on top of the 0 and rendered as "cu0".
    lx = x0 - 0.5
    note(ax, lx, ybox + hbox + 0.62, "cut at", size=11, color=ORANGE, ha="right")
    note(ax, lx, ybox - 0.42, "index", size=11, ha="right")
    note(ax, lx, ybox - 0.92, "from the end", size=11, color=MUTED, ha="right")

    note(ax, fig.get_size_inches()[0] / 2, 0.42,
         "The two numbers are cut positions, not items. Cut at 1 and at 4, "
         "and you keep what lies between: three names, not four.",
         size=11.5, color=INK)
    save(fig, path)


# --------------------------------------------------------------------------
def comprehension_to_loop(path):
    """Diagram 4: every comprehension is a loop, part for part."""
    fig, ax = canvas(11.5, 5.4)

    note(ax, 0.55, 5.1, "the comprehension", size=11.5, ha="left")
    code_run(ax, 0.55, 4.45, [("[ ", None), ("n * 2", BLUE), ("  ", None),
                              ("for n in numbers", ORANGE), ("  ", None),
                              ("if n > 10", PURPLE), ("]", None)])

    note(ax, 0.55, 3.45, "the same loop, written out", size=11.5, ha="left")
    code_run(ax, 0.55, 2.80, [("result = []", None)])
    code_run(ax, 0.55, 2.05, [("for n in numbers", ORANGE), (":", None)])
    code_run(ax, 0.55, 1.30, [("    ", None), ("if n > 10", PURPLE), (":", None)])
    code_run(ax, 0.55, 0.55, [("        result.append(", None),
                              ("n * 2", BLUE), (")", None)])

    note(ax, 5.75, 0.05,
         "The colours pair up. Note the order: what goes into the list is written "
         "first in the comprehension, but happens last in the loop.",
         size=11.5, color=INK)
    save(fig, path)



# --------------------------------------------------------------------------
def dict_vs_list(path):
    """Diagram 1: a list is found by position, a dictionary by name."""
    fig, ax = canvas(11, 4.4)
    ax.plot([5.4, 5.4], [0.5, 3.8], color="#cccccc", lw=1.2, ls=(0, (4, 4)))

    note(ax, 2.5, 3.95, "a list: found by position", size=12.5, color=INK, bold=True)
    for i, v in enumerate(["'ada'", "'grace'", "'alan'"]):
        box(ax, 0.6 + i * 1.35, 2.5, 1.3, 0.72, v, size=11)
        note(ax, 1.25 + i * 1.35, 2.25, str(i), size=12, color=INK)
    note(ax, 2.5, 1.5, "names[1]", size=13, color=BLUE, mono=True, bold=True)
    arrow(ax, (2.5, 1.75), (2.0, 2.4), color=BLUE)
    note(ax, 2.5, 1.05, "'grace'", size=12, color=BLUE, mono=True)

    note(ax, 8.3, 3.95, "a dictionary: found by name", size=12.5, color=INK, bold=True)
    for i, (k, v) in enumerate([("'ada'", "36"), ("'grace'", "45"), ("'alan'", "41")]):
        yy = 2.95 - i * 0.78
        box(ax, 6.2, yy, 1.5, 0.62, k, size=11)
        box(ax, 8.35, yy, 1.0, 0.62, v, size=11, fill="#ffffff")
        arrow(ax, (7.75, yy + 0.31), (8.3, yy + 0.31), lw=1.4)
    note(ax, 8.3, 0.98, "ages['grace']", size=13, color=ORANGE, mono=True, bold=True)
    # Rows sit at 2.95 / 2.17 / 1.39 and are 0.62 tall, so grace's value box
    # spans 2.17 to 2.79. Aim at its middle, not at the gap underneath it.
    arrow(ax, (8.4, 1.22), (8.8, 2.42), color=ORANGE)
    note(ax, 8.3, 0.6, "45", size=12, color=ORANGE, mono=True)

    note(ax, 5.4, 0.2,
         "A list asks which position. A dictionary asks which name. That is the "
         "whole difference.", size=11.5, color=INK)
    save(fig, path)


# --------------------------------------------------------------------------
def nested_dicts(path):
    """Diagram 2: the value can itself be a list or a dictionary."""
    fig, ax = canvas(11.5, 4.6)
    ax.plot([5.7, 5.7], [0.5, 4.0], color="#cccccc", lw=1.2, ls=(0, (4, 4)))

    note(ax, 2.6, 4.15, "a list inside a dictionary", size=12.5, color=INK, bold=True)
    for i, (k, v) in enumerate([("'eric'", "[3, 11, 19]"), ("'ever'", "[2, 4, 5]")]):
        yy = 3.0 - i * 0.95
        box(ax, 0.5, yy, 1.4, 0.7, k, size=11)
        box(ax, 2.4, yy, 2.5, 0.7, v, size=11, fill="#ffffff")
        arrow(ax, (1.95, yy + 0.35), (2.35, yy + 0.35), lw=1.4)
    note(ax, 2.6, 1.15, "favorite_numbers['eric'][0]", size=11.5, color=BLUE, mono=True)
    note(ax, 2.6, 0.78, "3", size=12, color=BLUE, mono=True)

    note(ax, 8.6, 4.15, "a dictionary inside a dictionary", size=12.5, color=INK, bold=True)
    box(ax, 6.0, 2.05, 1.5, 0.7, "'gabby'", size=11)
    ax.add_patch(FancyBboxPatch((7.95, 1.55), 3.1, 1.7,
                                boxstyle="round,pad=0.04,rounding_size=0.08",
                                linewidth=1.6, facecolor="#ffffff", edgecolor=EDGE))
    for i, (k, v) in enumerate([("'name'", "'gabby'"), ("'follower_num'", "13")]):
        yy = 2.72 - i * 0.62
        ax.text(8.15, yy, k, ha="left", va="center", fontsize=10, color=INK, **MONO)
        ax.text(10.85, yy, v, ha="right", va="center", fontsize=10, color=INK, **MONO)
    arrow(ax, (7.55, 2.4), (7.9, 2.4), lw=1.4)
    note(ax, 8.6, 1.15, "overall_users['gabby']['follower_num']", size=11.5,
         color=ORANGE, mono=True)
    note(ax, 8.6, 0.78, "13", size=12, color=ORANGE, mono=True)

    note(ax, 5.75, 0.2,
         "A value can be any structure, including another list or dictionary. "
         "Reach in one bracket at a time.", size=11.5, color=INK)
    save(fig, path)


# --------------------------------------------------------------------------
def boolean_mask(path):
    """Diagram 3: the mask is one True or False per row."""
    fig, ax = canvas(11.6, 4.8)
    rows = [("31", "Male"), ("45", "Female"), ("28", "Female"), ("52", "Male")]
    keep = [True, False, True, False]

    grid(ax, 0.4, 4.05, [["age", "gender"]] + [list(r) for r in rows], [1.1, 1.5])
    note(ax, 1.45, 4.25, "df", size=12, color=INK, mono=True, bold=True)

    note(ax, 4.5, 4.25, "df.age < 40", size=12, color=ORANGE, mono=True, bold=True)
    grid(ax, 3.7, 4.05, [["mask"]] + [["True" if k else "False"] for k in keep], [1.6],
         row_fills=[ORANGE if k else None for k in keep])

    note(ax, 8.6, 4.25, "df[df.age < 40]", size=12, color=BLUE, mono=True, bold=True)
    kept = [list(r) for r, k in zip(rows, keep) if k]
    grid(ax, 7.6, 4.05, [["age", "gender"]] + kept, [1.1, 1.5],
         row_fills=[BLUE] * len(kept))

    arrow(ax, (3.1, 2.6), (3.6, 2.6), color=ORANGE, lw=2)
    arrow(ax, (5.45, 2.6), (7.5, 2.6), color=BLUE, lw=2)
    note(ax, 6.5, 2.85, "keeps the True rows", size=11, color=BLUE)

    note(ax, 5.8, 0.55,
         "The comparison makes one True or False for every row. Putting it in "
         "brackets keeps the rows where it came out True.", size=11.5, color=INK)
    note(ax, 5.8, 0.2,
         "Each condition needs its own brackets, and it is & and |, never and / or.",
         size=11, color=MUTED)
    save(fig, path)


# --------------------------------------------------------------------------
def groupby_diagram(path):
    """Diagram 4: split, apply, combine."""
    fig, ax = canvas(12, 5.4)
    note(ax, 6, 5.1, 'df.groupby("marital-status")["capital-gain"].mean()',
         size=13, color=INK, mono=True, bold=True)

    data = [("Divorced", "0"), ("Married", "1200"), ("Divorced", "400"),
            ("Married", "800"), ("Married", "100")]
    tints = {"Divorced": PURPLE, "Married": ORANGE}
    note(ax, 1.75, 4.62, "1. split", size=12, color=INK, bold=True)
    grid(ax, 0.4, 4.35, [["marital", "gain"]] + [list(d) for d in data], [1.5, 1.2],
         row_h=0.54, row_fills=[tints[d[0]] for d in data])

    note(ax, 5.9, 4.62, "2. apply mean() to each group", size=12, color=INK, bold=True)
    for i, (g, vals, col) in enumerate([
            ("Divorced", "0, 400", PURPLE), ("Married", "1200, 800, 100", ORANGE)]):
        yy = 3.55 - i * 1.15
        box(ax, 4.2, yy, 1.6, 0.66, g, size=10.5, fill=tint(col), edge=col)
        note(ax, 6.15, yy + 0.33, vals, size=11, color=INK, mono=True, ha="left")
        arrow(ax, (3.25, yy + 0.33), (4.15, yy + 0.33), color=col, lw=1.6)

    note(ax, 10.3, 4.62, "3. combine", size=12, color=INK, bold=True)
    grid(ax, 9.0, 4.35, [["marital", "mean"], ["Divorced", "200"], ["Married", "700"]],
         [1.5, 1.2], row_h=0.54, row_fills=[PURPLE, ORANGE])
    arrow(ax, (8.3, 3.4), (8.9, 3.4), lw=2)

    note(ax, 6, 0.85,
         "One row per group, instead of one line of code per group.", size=12,
         color=INK)
    note(ax, 6, 0.42,
         "The repetitive version just above this in the notebook does the same "
         "thing by hand, one line per value.", size=11, color=MUTED)
    save(fig, path)


# --------------------------------------------------------------------------
def accumulator(path):
    """Diagram 5: before the loop, inside the loop, after the loop."""
    fig, ax = canvas(11.6, 4.8)
    note(ax, 6.2, 4.5, "words = ['the', 'old', 'man']", size=13, color=INK,
         mono=True, bold=True)

    rows = [["", "word", "len(word)", "total"],
            ["before", "", "", "0"],
            ["pass 1", "'the'", "3", "3"],
            ["pass 2", "'old'", "3", "6"],
            ["pass 3", "'man'", "3", "9"],
            ["after", "", "", "9"]]
    grid(ax, 2.7, 4.05, rows, [1.5, 1.5, 1.8, 1.3], row_h=0.55,
         row_fills=[FILL, None, None, None, FILL])

    note(ax, 2.45, 3.5, "start it off", size=10.5, ha="right")
    note(ax, 2.45, 2.12, "change it,\nonce per item", size=10.5, ha="right")
    note(ax, 2.45, 0.75, "use it", size=10.5, ha="right")

    note(ax, 5.8, 0.28,
         "Make the variable before the loop, change it inside, use it after. "
         "Almost every loop you write has this shape.", size=11.5, color=INK)
    save(fig, path)


# --------------------------------------------------------------------------
def name_and_value(path):
    """Diagram 7: a name is a label on a value."""
    fig, ax = canvas(11.2, 4.6)

    note(ax, 0.5, 4.3, 'message = "Hello Python world!"', size=13, color=INK,
         mono=True, bold=True, ha="left")
    name(ax, 1.35, 3.42, "message")
    box(ax, 1.75, 3.07, 3.7, 0.7, '"Hello Python world!"', size=11)
    arrow(ax, (1.45, 3.42), (1.72, 3.42))

    note(ax, 0.5, 2.42, 'message = "Hi"', size=13, color=INK, mono=True,
         bold=True, ha="left")
    name(ax, 1.35, 1.54, "message")
    box(ax, 1.75, 1.19, 1.5, 0.7, '"Hi"', size=11)
    arrow(ax, (1.45, 1.54), (1.72, 1.54), color=ORANGE)
    box(ax, 4.0, 1.19, 3.7, 0.7, '"Hello Python world!"', size=10.5,
        fill="#f4f4f4", edge="#bbbbbb")
    note(ax, 7.9, 1.54, "no longer reachable", size=10.5, color=MUTED, ha="left")

    note(ax, 5.6, 0.6,
         "The name is a label, not a box. Assigning again moves the label to a "
         "different value; it does not change the old one.", size=11.5, color=INK)
    note(ax, 5.6, 0.22,
         "This is why two names can end up on one list, and why changing that "
         "list is visible through both of them.", size=11, color=MUTED)
    save(fig, path)


# --------------------------------------------------------------------------
def json_four_names(path):
    """Diagram 8: dump, dumps, load, loads."""
    fig, ax = canvas(11, 4.7)
    box(ax, 4.2, 1.85, 2.6, 0.95, "a dictionary\nin Python", size=11.5, mono=False)
    box(ax, 0.4, 1.85, 2.3, 0.95, "a file\non disk", size=11.5, mono=False,
        fill="#f2f2f2", edge="#999999")
    box(ax, 8.3, 1.85, 2.3, 0.95, "a string\nin memory", size=11.5, mono=False,
        fill="#f2f2f2", edge="#999999")

    arrow(ax, (4.15, 2.55), (2.75, 2.55), color=BLUE, lw=1.8)
    note(ax, 3.45, 3.08, "json.dump(obj, f)", size=11, color=BLUE, mono=True)
    arrow(ax, (2.75, 2.05), (4.15, 2.05), color=BLUE, lw=1.8)
    note(ax, 3.45, 1.62, "json.load(f)", size=11, color=BLUE, mono=True)

    arrow(ax, (6.85, 2.55), (8.25, 2.55), color=ORANGE, lw=1.8)
    note(ax, 7.55, 3.08, "json.dumps(obj)", size=11, color=ORANGE, mono=True)
    arrow(ax, (8.25, 2.05), (6.85, 2.05), color=ORANGE, lw=1.8)
    note(ax, 7.55, 1.62, "json.loads(s)", size=11, color=ORANGE, mono=True)

    note(ax, 5.5, 0.95, "The s is for string.", size=13, color=INK, bold=True)
    note(ax, 5.5, 0.45,
         "dump and load take an open file. dumps and loads hand you, or take "
         "from you, a plain string.", size=11.5, color=INK)
    save(fig, path)


# --------------------------------------------------------------------------
def args_kwargs(path):
    """Diagram 9: * collects into a tuple, ** into a dictionary."""
    fig, ax = canvas(11.4, 5.0)

    note(ax, 0.5, 4.72, "adder(1, 2, 3, 4)", size=13, color=INK, mono=True,
         bold=True, ha="left")
    note(ax, 0.5, 4.3, "def adder(num_1, num_2, *nums):", size=12, color=MUTED,
         mono=True, ha="left")
    for i, (lbl, val, col) in enumerate([("num_1", "1", EDGE), ("num_2", "2", EDGE),
                                         ("nums", "(3, 4)", ORANGE)]):
        xx = 0.6 + i * 3.4
        box(ax, xx, 3.2, 1.5, 0.66, lbl, size=11, fill=FILL)
        box(ax, xx + 1.75, 3.2, 1.3, 0.66, val, size=11, fill="#ffffff",
            edge=col if col is ORANGE else EDGE)
        arrow(ax, (xx + 1.55, 3.53), (xx + 1.7, 3.53), color=col, lw=1.4)
    note(ax, 7.4, 2.95, "one tuple, however many are left over", size=10.5,
         color=ORANGE, ha="left")

    note(ax, 0.5, 2.25, "example_function('a', 'b', value_3='c', value_4='d')",
         size=13, color=INK, mono=True, bold=True, ha="left")
    note(ax, 0.5, 1.85, "def example_function(arg_1, arg_2, **kwargs):", size=12,
         color=MUTED, mono=True, ha="left")
    for i, (lbl, val) in enumerate([("arg_1", "'a'"), ("arg_2", "'b'")]):
        xx = 0.6 + i * 2.6
        box(ax, xx, 0.85, 1.4, 0.66, lbl, size=11, fill=FILL)
        box(ax, xx + 1.6, 0.85, 0.8, 0.66, val, size=11, fill="#ffffff")
        arrow(ax, (xx + 1.45, 1.18), (xx + 1.55, 1.18), lw=1.4)
    box(ax, 5.9, 0.9, 1.5, 0.66, "kwargs", size=11, fill=FILL)
    # Both pairs go inside the one box: an earlier version put the second pair
    # in a separate label, which straddled the box's bottom edge.
    box(ax, 7.65, 0.75, 3.4, 0.96,
        "{'value_3': 'c',\n 'value_4': 'd'}", size=10.5, fill="#ffffff", edge=PURPLE)
    arrow(ax, (7.45, 1.23), (7.6, 1.23), color=PURPLE, lw=1.4)
    note(ax, 5.9, 0.35, "one dictionary of the extra keyword arguments", size=10.5,
         color=PURPLE, ha="left")
    save(fig, path)


# --------------------------------------------------------------------------
def if_ladder(path):
    """Diagram 10: the first test that is true wins."""
    fig, ax = canvas(10.8, 4.3)
    note(ax, 5.4, 4.0, "dogs has 4 items", size=13, color=INK, mono=True, bold=True)

    rows = [
        ("if len(dogs) >= 5:", "False", "skipped", False),
        ("elif len(dogs) >= 3:", "True", "this one runs", True),
        ("else:", "", "never reached", False),
    ]
    for i, (code, val, fate, hit) in enumerate(rows):
        yy = 3.1 - i * 0.85
        col = ORANGE if hit else "#aaaaaa"
        ax.add_patch(FancyBboxPatch((0.5, yy - 0.3), 4.6, 0.62,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    linewidth=0, facecolor=col,
                                    alpha=0.18 if hit else 0.10, zorder=2))
        ax.text(0.7, yy, code, ha="left", va="center", fontsize=12.5, zorder=3,
                color=INK if hit else "#999999",
                fontweight="bold" if hit else "normal", **MONO)
        note(ax, 6.0, yy, val, size=12, color=col if hit else "#999999", mono=True)
        note(ax, 7.1, yy, fate, size=11, color=col if hit else "#999999", ha="left")

    note(ax, 5.4, 0.55,
         "Python takes the first test that is true and skips everything after it, "
         "so the order of your tests is the design.", size=11.5, color=INK)
    note(ax, 5.4, 0.18, "Put the strictest condition first.", size=11, color=MUTED)
    save(fig, path)


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    two_names_one_list("Day2/img/two_names_one_list.png")
    slicing("Day2/img/slicing_cuts.png")
    comprehension_to_loop("Day2/img/comprehension_to_loop.png")
    if_ladder("Day2/img/if_ladder.png")
    name_and_value("Day1/img/name_and_value.png")
    accumulator("Day1/img/accumulator.png")
    dict_vs_list("Day3/img/dict_vs_list.png")
    nested_dicts("Day3/img/nested_dicts.png")
    boolean_mask("Day4/img/boolean_mask.png")
    groupby_diagram("Day4/img/groupby.png")
    json_four_names("Day4/img/json_four_names.png")
    args_kwargs("Day4/img/args_kwargs.png")


if __name__ == "__main__":
    main()
