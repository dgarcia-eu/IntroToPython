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


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    two_names_one_list("Day2/img/two_names_one_list.png")
    slicing("Day2/img/slicing_cuts.png")
    comprehension_to_loop("Day2/img/comprehension_to_loop.png")


if __name__ == "__main__":
    main()
