"""Beat 6 (4.49 s): blocks stack; each one refines the previous block's output.

VO (scene-local s): "Now each block receives the previous block's output"
0.0-2.5 ("block" ~0.6, "output" ~2.3); "and continues to refine it further"
2.5-4.49 ("refine" ~3.3). No scene captions: VO captions are burned in later.
Opens on beat 5's end (bracketed matrix, VALUES[2]); ends on VALUES[3] with
nothing else on screen. Hero: the magenta flow line sweeping down the stack.

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh 06_stack.py Stack
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from _tokens import VALUES, build_matrix, word_labels, label

BEAT_SECONDS = 4.49
T_PREVIOUS = 1.1      # "the previous block's output": slabs stack in, land ~2.3
T_REFINE = 2.6        # "refine": the flow sweeps down, numbers tick, centred ~3.2
T_CLEAR = 3.8         # panels fade so beat 7 opens clean

PAD = 0.15            # label <-> panel edge
PANEL_BLEED = 0.25    # panel fill may run past the safe edges
SLAB_GAP = 0.25
CLOSE_FROM = 1.08     # "closes around": the panel starts this much larger
PANEL_STROKE = S.STROKE_AXIS * 2


def panel(left: float, right: float, bottom: float, top: float) -> RoundedRectangle:
    r = RoundedRectangle(corner_radius=0.2, width=right - left, height=top - bottom,
                         fill_color=S.BG_PANEL, fill_opacity=1,
                         stroke_color=S.FG_DIM, stroke_width=PANEL_STROKE)
    return r.move_to([(left + right) / 2, (bottom + top) / 2, 0])


class Stack(BocShortScene):
    def construct(self):
        st = self.stage
        m = build_matrix(st, values=VALUES[2], digits=True, bracketed=True)
        words = word_labels(m)
        xl, xr = st.get_left()[0] - PANEL_BLEED, st.get_right()[0] + PANEL_BLEED
        label_x = st.get_left()[0] + PAD

        # Block 1 closes around the matrix; its label sits above the words.
        tag1 = label("block 1", S.FG_DIM)
        top1 = words.get_top()[1] + PAD + tag1.height + PAD
        bottom1 = m.get_bottom()[1] - PAD
        block1 = panel(xl, xr, bottom1, top1)
        tag1.move_to([0, words.get_top()[1] + PAD + tag1.height / 2, 0]).align_to(
            [label_x, 0, 0], LEFT)
        opener = block1.copy().scale(CLOSE_FROM).set_fill(opacity=0).set_stroke(opacity=0)

        # Blocks 2 and 3: short slabs filling the lower region.
        slab_top = bottom1 - SLAB_GAP - 0.05
        slab_h = (slab_top - st.get_bottom()[1] - SLAB_GAP) / 2
        slabs, tags = VGroup(), VGroup()
        for i in range(2):
            top = slab_top - i * (slab_h + SLAB_GAP)
            slabs.add(panel(xl, xr, top - slab_h, top))
            tags.add(label(f"block {i + 2}", S.FG_DIM).move_to(slabs[-1]).align_to(
                [label_x, 0, 0], LEFT))

        # Frame 0: matrix + words (panel pre-added invisible so it layers behind).
        self.add(opener, m, words)
        self.play(Transform(opener, block1), FadeIn(tag1), run_time=S.BEAT)

        # "previous block's output": two more blocks stack below.
        self.hold_until(T_PREVIOUS)
        self.play(LaggedStart(*[FadeIn(VGroup(s, t), shift=DOWN * 0.4) for s, t in zip(slabs, tags)],
                              lag_ratio=0.35), run_time=S.HOLD)

        # "refine it further": the output flows down the stack; the numbers tick.
        self.hold_until(T_REFINE)
        y0, y1 = m.get_top()[1], slabs[-1].get_bottom()[1]
        fx0, fx1 = st.get_left()[0] + PAD, st.get_right()[0] - PAD
        sweep = ValueTracker(0)

        def flow() -> Line:
            a = sweep.get_value()
            ln = Line([fx0, 0, 0], [fx1, 0, 0], color=S.STRUCTURE,
                      stroke_width=S.STROKE_STRUCTURE * 1.6)
            ln.set_stroke(opacity=min(1.0, 4 * a, 4 * (1 - a)))
            return ln.move_to([(fx0 + fx1) / 2, interpolate(y0, y1, a), 0])

        line = always_redraw(flow)
        self.add(line)
        self.play(sweep.animate.set_value(1), m.count_to(VALUES[3]), run_time=S.HOLD)
        self.remove(line)

        # Panels fade: beat 7 opens on words + matrix alone. One FadeOut per
        # mobject: a fresh VGroup would be added on top of the matrix and its
        # fill would dim the numbers while it fades.
        self.hold_until(T_CLEAR)
        self.play(*[FadeOut(x) for x in (opener, tag1, *slabs, *tags)], run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
