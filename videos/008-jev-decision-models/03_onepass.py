"""Beat 3 (13.11 s): an LLM decides token by token, one pass each; Jev scores
every choice in one pass.

VO (10.14-23.25 s): "This is exciting 'cause this is much more efficient than
what an LLM does. An LLM decides by generating token by token, and every token
is another pass through the whole model. Jev scores all the choices in one
single pass, so it's fast and cheap."
Frame 0: the stage is split, "LLM" on top, "decision model" below, each with a
tiny network and a pass counter. The LLM's output types one glyph per QUICK;
every glyph pulses the LLM net cyan and ticks its counter (to 30). On "Jev" the
input card rides into the bottom net once: one magenta flash, "passes 1" in
magenta (the hero), and the three bars fill together by "pass". On "fast" the
tag "171 ms vs 1.7 s / same accuracy" appears under the split.

Render:
    cd videos/008-jev-decision-models && uv run --no-sync manim -qh 03_onepass.py OnePass
    # -> media/videos/03_onepass/1920p30/OnePass.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import EDGE_WIDTH, flow_arrow, label
import _parts as P

BEAT_SECONDS = 13.11   # exact VO window of this beat
T_JEV = 9.24           # VO: "Jev" (silence ends 9.236); the card rides into the net
T_PASS = 11.36         # VO: "pass" ends; the bars are full here
T_FAST = 11.7          # VO: "fast"; the latency tag appears

STREAM = ['{"urgent": "yes",', '"reason": "ceo"}']   # the LLM's token stream, 2 lines
N_TOKENS = int(T_JEV // S.QUICK)                      # one glyph per QUICK until "Jev"
PROBS = [0.91, 0.06, 0.03]

NET_W, NET_BOX_H, NET_GAP = 1.6, 0.36, 0.22   # the tiny 3-box network
COL_GAP = 0.5                                 # net column -> output column
LABEL_GAP = 0.08                              # half label -> content row
TAG_H = 1.44                                  # two label lines + air, at the stage floor
BARS_W, BARS_SCALE = 5.0, 0.9                 # ProbBars fits the bottom-right area at 0.9


def net_glyph() -> VGroup:
    """Three dim boxes, teal flow bottom to top. `.boxes`, `.arrows`."""
    boxes = VGroup(*[
        RoundedRectangle(corner_radius=0.1, width=NET_W, height=NET_BOX_H, fill_color=S.BG_PANEL,
                         fill_opacity=1, stroke_color=S.FG_DIM, stroke_width=EDGE_WIDTH)
        for _ in range(3)
    ]).arrange(UP, buff=NET_GAP)
    arrows = VGroup(*[flow_arrow(a.get_top(), b.get_bottom()) for a, b in zip(boxes, boxes[1:])])
    g = VGroup(boxes, arrows)
    g.boxes, g.arrows = boxes, arrows
    return g


def pulse(net: VGroup, color: str) -> AnimationGroup:
    """The whole net's stroke flashes `color` once and settles back."""
    return AnimationGroup(*[
        b.animate(rate_func=there_and_back).set_stroke(color=color, width=EDGE_WIDTH * 2)
        for b in net.boxes
    ])


class OnePass(BocShortScene):
    def half(self, name: str, top: float, bottom: float) -> dict:
        """One half of the split: label top-left, net + counter left, output right."""
        left = self.stage.get_left()[0]
        title = label(name, S.FG_DIM).align_to([left, top, 0], UL)
        content_top = title.get_bottom()[1] - LABEL_GAP
        net = net_glyph().align_to([left, content_top, 0], UL)
        counter = VGroup(P.mono("passes 0", S.FG_DIM))
        counter.next_to(net, DOWN, buff=0.1).align_to(net, LEFT)
        out = Rectangle(width=self.stage.get_right()[0] - (left + NET_W + COL_GAP),
                        height=content_top - bottom, stroke_opacity=0, fill_opacity=0)
        out.align_to([left + NET_W + COL_GAP, content_top, 0], UL)
        return dict(title=title, net=net, counter=counter, out=out)

    def tick(self, h: dict, n: int, color: str = S.FG_DIM) -> None:
        new = P.mono(f"passes {n}", color).next_to(h["net"], DOWN, buff=0.1).align_to(h["net"], LEFT)
        h["counter"].remove(*h["counter"].submobjects)
        h["counter"].add(new)

    def construct(self):
        top, bottom = self.stage.get_top()[1], self.stage.get_bottom()[1]
        half_h = (top - bottom - TAG_H) / 2
        llm = self.half("LLM", top, top - half_h)
        jev = self.half("decision model", top - half_h, top - 2 * half_h)
        divider = Line(self.stage.get_left(), self.stage.get_right(), color=S.FG_DIM,
                       stroke_width=S.STROKE_AXIS).set_stroke(opacity=S.OP_AXIS)
        divider.move_to([self.stage.get_center()[0], top - half_h, 0])

        # The LLM's token stream: two mono lines laid out now, revealed glyph by glyph.
        lines = VGroup(*[P.mono(l) for l in STREAM]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lines.align_to(llm["out"], UL)
        glyphs = [g for line in lines for g in line]

        card = P.text_card(["urgent?", "yes/no/later"]).move_to(jev["out"]).align_to(jev["out"], RIGHT)
        bars = P.ProbBars(["yes", "no", "later"], width=BARS_W).scale(BARS_SCALE)
        bars.move_to(jev["out"]).align_to(jev["out"], RIGHT)

        for h in (llm, jev):
            self.add(h["title"], h["net"], h["counter"])
        self.add(divider, card)

        # "token by token ... every token is another pass": one glyph, one pass.
        for i in range(N_TOKENS):
            self.tick(llm, i + 1)
            self.play(FadeIn(glyphs[i]), pulse(llm["net"], S.HIGHLIGHT), run_time=S.QUICK)

        # "Jev scores all the choices in one single pass": the card rides into the net once.
        self.hold_until(T_JEV)
        into = card.copy().scale(0.25).move_to(jev["net"].boxes[0]).set_opacity(0)
        self.play(Transform(card, into), run_time=S.BEAT)
        self.remove(card)
        self.tick(jev, 1, S.STRUCTURE)
        self.play(pulse(jev["net"], S.STRUCTURE), FadeIn(bars), run_time=S.QUICK)
        self.hold_until(T_PASS - S.HOLD)
        self.play(bars.fill_to(PROBS), run_time=S.HOLD)

        # "fast and cheap": the measured tag at the stage floor.
        self.hold_until(T_FAST)
        tag = VGroup(label("171 ms vs 1.7 s", S.FG_DIM), label("same accuracy", S.FG_DIM))
        tag.arrange(DOWN, buff=0.08).move_to(self.stage).align_to(self.stage, DOWN)
        self.play(FadeIn(tag), run_time=S.BEAT)

        self.hold_until(BEAT_SECONDS)
