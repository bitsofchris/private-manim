"""Residual stream — a token flows through the model.

The token "pickle" becomes an embedding vector (numeric column). That vector
flows through stacked weight matrices (layers). At each layer, a few entries
in the matrix light up and write new numbers into the next vector. The
running line of vectors IS the residual stream.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 06c_residual_stream.py ResidualStream
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    Rectangle,
    Succession,
    Text,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene


N_LAYERS = 3
VEC_DIM = 6

# Vector cells (with numbers).
V_CELL_W = 0.78
V_CELL_H = 0.46

# Layer (weight matrix) cells.
M_CELL = 0.34
M_ROWS = VEC_DIM
M_COLS = VEC_DIM

# Stage spacing — distance between successive vector-column centers.
STAGE_DX = 3.5


def _fmt(v: float) -> str:
    return f"{v:+.2f}"


def _vector_column(values, center, color=S.DATA, label: str | None = None) -> VGroup:
    cx, cy = center
    rows = VGroup()
    top = cy + (len(values) - 1) * V_CELL_H / 2
    for i, v in enumerate(values):
        rect = Rectangle(
            width=V_CELL_W,
            height=V_CELL_H,
            stroke_color=S.FG_DIM,
            stroke_width=1.2,
            fill_color=color,
            fill_opacity=float(np.clip(abs(v), 0.12, 0.85)),
        ).move_to([cx, top - i * V_CELL_H, 0])
        num = Text(_fmt(v), font="Menlo", font_size=18, color=S.FG).move_to(rect)
        rows.add(VGroup(rect, num))
    group = VGroup(rows)
    if label is not None:
        lbl = Text(label, font=S.FONT, font_size=16, color=S.FG_DIM)
        lbl.next_to(rows, DOWN, buff=0.15)
        group.add(lbl)
    return group


def _matrix_grid(center) -> VGroup:
    cx, cy = center
    cells = VGroup()
    top = cy + (M_ROWS - 1) * M_CELL / 2
    left = cx - (M_COLS - 1) * M_CELL / 2
    for i in range(M_ROWS):
        for j in range(M_COLS):
            cell = Rectangle(
                width=M_CELL,
                height=M_CELL,
                stroke_color=S.STRUCTURE,
                stroke_width=0.8,
                fill_color=S.STRUCTURE,
                fill_opacity=0.06,
            ).move_to([left + j * M_CELL, top - i * M_CELL, 0])
            cells.add(cell)
    return cells


class ResidualStream(BocScene):
    def construct(self):
        rng = np.random.default_rng(S.SEED)
        cy = -0.2

        # Center the whole pipeline horizontally.
        total_w = N_LAYERS * STAGE_DX
        x_embed = -total_w / 2

        # 1. Input word.
        word = Text('"pickle"', font="Menlo", font_size=32, color=S.FG)
        word.move_to([x_embed, cy + 2.6, 0])
        self.play(FadeIn(word), run_time=S.QUICK)

        cap1 = self.show_caption("a token becomes a vector of numbers")

        # 2. Embedding column with numeric values in [-1, 1].
        embed_vals = rng.uniform(-1.0, 1.0, VEC_DIM)
        embed = _vector_column(embed_vals, (x_embed, cy), label="embedding")
        word_to_embed = Arrow(
            word.get_bottom() + 0.05 * DOWN,
            embed[0].get_top() + 0.05 * UP,
            color=S.FG_DIM, stroke_width=2, buff=0.05,
        )
        self.play(GrowArrow(word_to_embed), run_time=S.QUICK)
        self.play(FadeIn(embed[0], lag_ratio=0.08), Write(embed[1]), run_time=S.BEAT)
        self.beat("BEAT")
        self.hide_caption(cap1)

        # 3. Each layer: pulse the input, light up a few matrix cells, write new column.
        cap2 = self.show_caption("each layer updates the vector")

        prev_vals = embed_vals
        prev_col = embed[0]
        keep: list[VGroup] = []

        for k in range(N_LAYERS):
            layer_x = x_embed + (k + 0.5) * STAGE_DX
            next_x = x_embed + (k + 1) * STAGE_DX

            matrix = _matrix_grid((layer_x, cy))
            layer_lbl = Text(f"layer {k + 1}", font=S.FONT, font_size=16, color=S.FG_DIM)
            layer_lbl.next_to(matrix, UP, buff=0.18)

            arr_in = Arrow(
                prev_col.get_right() + 0.02 * RIGHT,
                matrix.get_left() + 0.02 * LEFT,
                color=S.FG_DIM, stroke_width=2, buff=0.05,
            )
            self.play(FadeIn(matrix), Write(layer_lbl), GrowArrow(arr_in), run_time=S.QUICK)

            # Pulse the input vector — it "flows in".
            self.play(Indicate(prev_col, color=S.HIGHLIGHT, scale_factor=1.04), run_time=S.QUICK)

            # Light up a handful of matrix cells in sequence.
            hot_idx = rng.choice(len(matrix), size=7, replace=False)
            flashes = [
                Indicate(matrix[i], color=S.STRUCTURE, scale_factor=1.25)
                for i in hot_idx
            ]
            self.play(AnimationGroup(*flashes, lag_ratio=0.12), run_time=0.9)

            # New activation = previous + small delta. Stays in [-1, 1] roughly.
            delta = rng.normal(0, 0.25, VEC_DIM)
            new_vals = np.clip(prev_vals + delta, -0.99, 0.99)
            label = "activation vector" if k == N_LAYERS - 1 else None
            color = S.DATA if k < N_LAYERS - 1 else S.HIGHLIGHT
            new_col = _vector_column(new_vals, (next_x, cy), color=color, label=label)

            arr_out = Arrow(
                matrix.get_right() + 0.02 * RIGHT,
                new_col[0].get_left() + 0.02 * LEFT,
                color=S.FG_DIM, stroke_width=2, buff=0.05,
            )
            self.play(GrowArrow(arr_out), run_time=S.QUICK)
            # Cells appear, numbers write in.
            self.play(FadeIn(new_col[0], lag_ratio=0.10), run_time=S.BEAT)
            self.play(Write(VGroup(*[c[1] for c in new_col[0]])), run_time=S.BEAT)
            self.beat("QUICK")

            keep.extend([matrix, layer_lbl, arr_in, arr_out, new_col])
            prev_vals = new_vals
            prev_col = new_col[0]

        self.beat("BEAT")
        self.hide_caption(cap2)

        # 4. Residual stream sweep underneath.
        cap3 = self.show_caption("this running line of vectors is the residual stream")
        last_col = keep[-1]
        stream_y = cy - V_CELL_H * VEC_DIM / 2 - 1.0
        stream = Arrow(
            [embed[0].get_x() - 0.2, stream_y, 0],
            [last_col[0].get_x() + 0.2, stream_y, 0],
            color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE, buff=0,
        )
        stream_lbl = Text(
            "residual stream", font=S.FONT, font_size=20,
            color=S.STRUCTURE, slant="ITALIC",
        ).next_to(stream, DOWN, buff=0.12)
        self.play(GrowArrow(stream), FadeIn(stream_lbl), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap3)

        all_objs = VGroup(word, word_to_embed, embed, *keep, stream, stream_lbl)
        self.play(FadeOut(all_objs), run_time=S.BEAT)
