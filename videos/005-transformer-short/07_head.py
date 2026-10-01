"""Beat 7 (8.83 s): a task-specific head turns the final representations into
whatever the training objective asks for.

VO (scene-local s): "Now the final representations are not necessarily
predictions" 0.03-2.93 ("not" ~2.0); "but a task specific output layer"
2.93-5.0 ("output layer" ~4.3); "will turn these representations" 5.0-6.4;
"into whatever the training objective is asking for" 6.4-8.69.
Opens on beat 6's end (bracketed matrix, VALUES[3]). Last beat: the final
frame is still and clean. Hero: the magenta head panel (+ its feed arrow).

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh 07_head.py Head
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import hero_arrow
from _tokens import VALUES, TARGET, NEXT_TOKENS, build_matrix, word_labels, label

BEAT_SECONDS = 8.83
T_HEAD = 3.4          # "output layer" ~4.3: the head lands at 4.6
T_BARS = 5.0          # "turn these representations": bars grow out
T_NEXT = 6.4          # "whatever the training objective": label flips...
T_CLASS = 7.2
T_NUMBER = 8.0
OBJECTIVES = ["next\ntoken", "class", "number"]
NUMBER_VALUE = "+0.7"  # the single regression output shown for "number"

HEAD_W = 3.2
HEAD_PAD = 0.1        # head panel <-> stage bottom
ARROW_GAP = 0.12      # column bottom -> arrow tail
ARROW_LEN = 0.55
ROW_PITCH = 0.8
BAR_H = 0.45
BAR_BUFF = 0.25       # word label -> bar, and bar -> head
PULSE_SCALE = 1.03    # Indicate on a 7-unit-wide matrix: barely larger


def head_label(s: str) -> Text:
    return label(s, S.STRUCTURE)


class Head(BocShortScene):
    def construct(self):
        st = self.stage
        m = build_matrix(st, values=VALUES[3], digits=True, bracketed=True)
        words = word_labels(m)
        self.add(m, words)
        sat = m.columns[TARGET]

        # Head panel under the sat column, fed by a thin arrow from it.
        head_top = sat.get_bottom()[1] - ARROW_GAP - ARROW_LEN
        head_bottom = st.get_bottom()[1] + HEAD_PAD
        head_x = min(sat.get_x(), st.get_right()[0] - HEAD_W / 2)
        head = RoundedRectangle(corner_radius=0.2, width=HEAD_W, height=head_top - head_bottom,
                                fill_color=S.BG_PANEL, fill_opacity=1,
                                stroke_color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE)
        head.move_to([head_x, (head_top + head_bottom) / 2, 0])
        tag = head_label("head").move_to(head)
        feed = hero_arrow(sat.get_bottom() + DOWN * ARROW_GAP, [sat.get_x(), head_top, 0],
                          stroke_width=S.STROKE_AXIS * 2, max_tip_length_to_length_ratio=0.4,
                          max_stroke_width_to_length_ratio=20)

        # Next-token rows left of the head: word, then a teal bar of width ~ p.
        names = VGroup(*[label(w) for w, _ in NEXT_TOKENS])
        bar_x0 = st.get_left()[0] + max(n.width for n in names) + BAR_BUFF
        avail = head.get_left()[0] - BAR_BUFF - bar_x0
        scale = avail / max(p for _, p in NEXT_TOKENS)
        ys = [0.0, 0.0, 0.0]
        y_mid = (m.get_bottom()[1] + st.get_bottom()[1]) / 2
        bars = VGroup()
        for i, ((w, p), n) in enumerate(zip(NEXT_TOKENS, names)):
            y = y_mid + (1 - i) * ROW_PITCH
            n.move_to([0, y, 0]).align_to(st, LEFT)
            bar = Rectangle(width=p * scale, height=BAR_H, fill_color=S.DATA, fill_opacity=S.OP_DATA,
                            stroke_width=0).move_to([bar_x0 + p * scale / 2, y, 0])
            bars.add(bar)
        rows = VGroup(*[VGroup(n, b) for n, b in zip(names, bars)])

        # "final representations": the whole matrix pulses. Nothing is predicted yet.
        self.play(Indicate(m, color=S.HIGHLIGHT, scale_factor=PULSE_SCALE), run_time=S.HOLD)

        # "output layer": the head appears under the last token, fed from it.
        self.hold_until(T_HEAD)
        self.play(FadeIn(head), FadeIn(tag), GrowArrow(feed), run_time=S.HOLD)

        # "turn these representations": a distribution grows out of the head.
        self.hold_until(T_BARS)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(n), GrowFromEdge(b, LEFT)) for n, b in rows],
                              lag_ratio=0.3), run_time=S.HOLD)

        # "whatever the training objective is asking for": the same head,
        # relabelled: next token -> class -> number (a single value).
        for t, name in zip((T_NEXT, T_CLASS, T_NUMBER), OBJECTIVES):
            self.hold_until(t)
            # A different word is a different label: fade-swap, never morph
            # glyphs (rule 8). Bars leave before the single value arrives.
            new_tag = head_label(name).move_to(head)
            if name == "number":
                value = label(NUMBER_VALUE, S.DATA).move_to([(st.get_left()[0] + head.get_left()[0]) / 2, y_mid, 0])
                self.play(FadeOut(tag), *[FadeOut(n) for n in names], *[FadeOut(b) for b in bars],
                          run_time=S.QUICK)
                self.play(FadeIn(new_tag), FadeIn(value), run_time=S.QUICK)
            else:
                self.play(FadeOut(tag), run_time=S.QUICK)
                self.play(FadeIn(new_tag), run_time=S.QUICK)
            tag = new_tag
        self.hold_until(BEAT_SECONDS)
