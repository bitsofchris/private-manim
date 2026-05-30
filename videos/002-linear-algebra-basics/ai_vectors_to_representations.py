"""Matrices are learned moves that make vector data more useful.

Viewer takeaway: vectors hold information; learned matrices reshape that
information into representations the model can use.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql ai_vectors_to_representations.py AIVectorsToRepresentations
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import hero_arrow


def txt(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


def card(title: str, body: str, color: str) -> VGroup:
    box = RoundedRectangle(
        width=2.6,
        height=0.9,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=S.STROKE_AXIS,
        fill_color=S.BG_PANEL,
        fill_opacity=S.OP_GHOST,
    )
    label = VGroup(
        txt(title, color, scale=S.TAG_SCALE),
        txt(body, S.FG_DIM, scale=0.32),
    ).arrange(DOWN, buff=0.08)
    return VGroup(box, label.move_to(box))


def matrix_block(name: str) -> VGroup:
    cells = VGroup()
    values = [["0.7", "-1.2", "0.4"], ["1.5", "0.2", "-0.8"], ["-0.3", "0.9", "1.1"]]
    for r, row in enumerate(values):
        rendered = VGroup()
        for value in row:
            square = Rectangle(
                width=0.48,
                height=0.34,
                stroke_color=S.STRUCTURE,
                stroke_width=S.STROKE_AXIS,
                fill_color=S.BG_PANEL,
                fill_opacity=S.OP_GHOST,
            )
            rendered.add(VGroup(square, txt(value, S.FG_DIM, scale=0.28).move_to(square)))
        rendered.arrange(RIGHT, buff=0)
        cells.add(rendered)
    cells.arrange(DOWN, buff=0)
    label = txt(name, S.STRUCTURE).next_to(cells, UP, buff=0.16)
    return VGroup(label, cells)


class AIVectorsToRepresentations(BocScene):
    def construct(self):
        title = txt("why matrices matter for AI", S.FG).to_corner(UL, buff=0.28)
        raw = VGroup(
            card("token", "embedding vector", S.DATA),
            card("image patch", "pixel feature vector", S.DATA),
            card("feature row", "tabular vector", S.DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(LEFT, buff=0.55).shift(DOWN * 0.1)
        raw_label = txt("raw vector data", S.DATA).next_to(raw, UP, buff=0.22)

        learned = matrix_block("learned W").move_to(ORIGIN).shift(UP * 0.25)
        questions = VGroup(
            txt("amplify useful directions?", S.FG_DIM, scale=S.TAG_SCALE),
            txt("ignore noise?", S.FG_DIM, scale=S.TAG_SCALE),
            txt("mix features together?", S.FG_DIM, scale=S.TAG_SCALE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(learned, DOWN, buff=0.42)

        useful = VGroup(
            card("attention", "query/key/value spaces", S.STRUCTURE),
            card("vision", "edge and texture features", S.STRUCTURE),
            card("prediction", "task-useful features", S.STRUCTURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.55).shift(DOWN * 0.1)
        useful_label = txt("more useful representations", S.STRUCTURE).next_to(useful, UP, buff=0.22)

        arrows_in = VGroup()
        arrows_out = VGroup()
        for item in raw:
            arrows_in.add(hero_arrow(item.get_right() + RIGHT * 0.08, learned.get_left() + LEFT * 0.08, color=S.DATA, stroke_width=S.STROKE_AXIS))
        for item in useful:
            arrows_out.add(hero_arrow(learned.get_right() + RIGHT * 0.08, item.get_left() + LEFT * 0.08, color=S.STRUCTURE, stroke_width=S.STROKE_AXIS))

        cap = self.show_caption("AI starts with data encoded as vectors.")
        self.play(FadeIn(title), FadeIn(raw_label), LaggedStart(*[FadeIn(item) for item in raw], lag_ratio=0.15), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("Training learns matrices that move those vectors.")
        self.play(LaggedStart(*[Create(arrow) for arrow in arrows_in], lag_ratio=0.08), FadeIn(learned), run_time=S.HOLD)
        self.play(LaggedStart(*[FadeIn(q) for q in questions], lag_ratio=0.18), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("The move makes useful structure easier to read.")
        self.play(LaggedStart(*[Create(arrow) for arrow in arrows_out], lag_ratio=0.08), FadeIn(useful_label), run_time=S.BEAT)
        self.play(LaggedStart(*[FadeIn(item) for item in useful], lag_ratio=0.15), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap)

        self.play(FadeOut(questions), run_time=S.BEAT)
        closing = VGroup(
            txt("Vectors hold information.", S.DATA),
            txt("Matrices reshape it into forms the model can use.", S.STRUCTURE),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(closing), run_time=S.HOLD)
        self.beat("HOLD")
