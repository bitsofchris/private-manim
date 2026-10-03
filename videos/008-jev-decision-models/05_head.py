"""Beat 5 (13.69 s): a decision model is a classifier head on a language model; anyone can train one.

VO (33.78-47.47 s): "Jev is one company's version, a specific implementation of
this decision model as a classifier. But the bigger idea is that we've gotten
really good at building rich representations with language models, and a
decision model is just a classifier on top of them. Anyone can train one."
Frame 0: a small tree: a "decision model" box with a connector down to a
magenta "Jev" chip, its child; Jev pulses on "Jev" and the connector lights
on "implementation". On "bigger idea" the parent box opens into the dim
transformer stack and Jev slides up to a badge row. On "rich representations" the teal flow pulses. On
"classifier" the magenta decision head drops onto the stack in place of the
LM head (Linear), the teal arrow from the stack feeding it. On "Anyone" two
more badges join Jev. Hero: the decision head.

Render:
    cd videos/008-jev-decision-models && uv run --no-sync manim -qh 05_head.py Head
    # -> media/videos/05_head/1920p30/Head.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import build_block, op_box, label
from _parts import chip_text

BEAT_SECONDS = 13.69   # exact VO window of this beat
T_IMPL = 2.75          # VO: "implementation"; the parent->child connector lights
T_BIGGER = 4.95        # VO: "bigger" (idea)
T_RICH = 7.10          # VO: "rich" (representations)
T_CLASSIFIER = 10.60   # VO: "classifier"; the head lands on "on top" (~11.2)
T_ANYONE = 12.20       # VO: "Anyone" (can train one)

BOX_PAD_W = 0.3        # match transformer.op_box proportions for the beat-2 box
BOX_PAD_H = 0.08
STACK_FRAC = 0.75      # the diagram fills the lower 75% of the stage; badges live above
CHIP_BUFF = 0.15       # three chips just fit the safe width at this spacing
TREE_DROP = 0.9        # connector length from the parent box to the Jev child
MODELS = ["Laya", "CLM-8B"]


class Head(BocShortScene):
    def construct(self):
        # Frame 0: a tree. The category on top, Jev hanging off it as one child.
        ref = label("decision model")
        box = op_box("decision model", ref.width + 2 * BOX_PAD_W, ref.height + 2 * BOX_PAD_H)
        box.move_to(self.stage).shift(UP * TREE_DROP)
        jev = chip_text("Jev")
        jev.box.set_stroke(S.STRUCTURE)
        jev.next_to(box, DOWN, buff=TREE_DROP)
        link = Line(box.get_bottom(), jev.get_top(), color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 3)
        self.add(box, link, jev)

        # "Jev": the child pulses.
        self.play(jev.animate(rate_func=there_and_back).scale(1.15), run_time=S.BEAT)

        # "specific implementation": the parent -> child link lights up once.
        self.hold_until(T_IMPL)
        self.play(link.animate(rate_func=there_and_back).set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE),
                  run_time=S.BEAT)

        # Layout for the open box: the stack in the lower part of the stage, badges above.
        stack_rect = Rectangle(width=self.stage.width, height=self.stage.height * STACK_FRAC,
                               stroke_opacity=0, fill_opacity=0)
        stack_rect.move_to(self.stage).align_to(self.stage, DOWN)
        d = build_block(stack_rect)
        # Lay the badge row out on a stand-in for Jev so the real badge stays put until it moves.
        badges = VGroup(jev.copy(), *[chip_text(m, S.FG_DIM) for m in MODELS])
        badges.arrange(RIGHT, buff=CHIP_BUFF).move_to([
            self.safe.get_center()[0], (d.get_top()[1] + self.safe.get_top()[1]) / 2, 0])
        jev_slot, others = badges[0], VGroup(*badges[1:])

        # "bigger idea": the box opens into the transformer stack; the badge moves aside.
        self.hold_until(T_BIGGER)
        self.play(ReplacementTransform(box, d), jev.animate.move_to(jev_slot), FadeOut(link),
                  run_time=S.HOLD)

        # "rich representations": the teal flow through the stack pulses once.
        self.hold_until(T_RICH)
        self.play(Indicate(d.flow, color=S.HIGHLIGHT, scale_factor=1.05), run_time=S.BEAT)

        # "classifier on top of them": the magenta decision head replaces the LM head.
        linear = d.rows["head"]
        hw = label("decision head").width + 2 * BOX_PAD_W
        head = op_box("decision head", hw, linear.height).move_to(linear)
        head.box.set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE)
        self.hold_until(T_CLASSIFIER)
        self.play(FadeOut(linear, run_time=S.BEAT),
                  FadeIn(head, shift=DOWN * 0.4, run_time=S.BEAT))

        # "Anyone can train one": two more badges beside Jev; Jev is one of many now.
        self.hold_until(T_ANYONE)
        self.play(FadeIn(others), jev.box.animate.set_stroke(S.FG_DIM), run_time=S.BEAT)

        self.hold_until(BEAT_SECONDS)
