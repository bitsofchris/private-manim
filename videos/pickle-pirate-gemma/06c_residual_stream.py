"""Residual stream — multi-token flow + next-token prediction.

Input "pickles taste good" is split into 3 tokens. Each token has its own
embedding and its own residual stream, flowing left-to-right in parallel
through stacked layers. Only the last token ("good") shows numeric values
to keep the frame clean. After the final layer, we isolate that activation
and project it through the unembedding matrix W_U to get logits over a
small vocabulary — the top one is the model's predicted next token.

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
    Text,
    Transform,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene


TOKENS = ["pickles", "taste", "good"]
N_LAYERS = 1   # one detailed layer, then a "× many layers" stack
VEC_DIM = 4

# Token vector cells (horizontal row per token).
V_CELL_W = 0.62
V_CELL_H = 0.42
ROW_GAP = 0.20

# Layer block (matrix grid) — drawn as a tall rectangle spanning all streams.
M_CELL = 0.26
M_COLS = 4
M_ROWS = 11

STAGE_DX = 4.6  # x-distance between successive activation-row centers


def _fmt(v: float) -> str:
    return f"{v:.2f}"


def _row_y(stream_idx: int, cy: float) -> float:
    n = len(TOKENS)
    top = cy + (n - 1) * (V_CELL_H + ROW_GAP) / 2
    return top - stream_idx * (V_CELL_H + ROW_GAP)


def _vector_row(values, center, color=S.STRUCTURE) -> VGroup:
    """Array-of-numbers row in the magenta/structure style. No heat-map."""
    cx, cy = center
    left = cx - (VEC_DIM - 1) * V_CELL_W / 2
    cells = VGroup()
    for j, v in enumerate(values):
        rect = Rectangle(
            width=V_CELL_W, height=V_CELL_H,
            stroke_color=color, stroke_width=1.4,
            fill_color=color,
            fill_opacity=0.08,
        ).move_to([left + j * V_CELL_W, cy, 0])
        num = Text(_fmt(v), font="Menlo", font_size=14, color=S.FG).move_to(rect)
        cells.add(VGroup(rect, num))
    return cells


def _layer_block(cx, cy_center, height) -> VGroup:
    block = Rectangle(
        width=M_COLS * M_CELL + 0.18,
        height=height,
        stroke_color=S.STRUCTURE, stroke_width=2,
        fill_color=S.STRUCTURE, fill_opacity=0.06,
    ).move_to([cx, cy_center, 0])
    inner = VGroup()
    grid_h = M_ROWS * M_CELL
    grid_w = M_COLS * M_CELL
    top = cy_center + grid_h / 2 - M_CELL / 2
    left = cx - grid_w / 2 + M_CELL / 2
    for i in range(M_ROWS):
        for j in range(M_COLS):
            inner.add(Rectangle(
                width=M_CELL, height=M_CELL,
                stroke_color=S.STRUCTURE, stroke_width=0.6,
                fill_color=S.STRUCTURE, fill_opacity=0.10,
            ).move_to([left + j * M_CELL, top - i * M_CELL, 0]))
    return VGroup(block, inner)


class ResidualStream(BocScene):
    def construct(self):
        rng = np.random.default_rng(S.SEED)
        cy = 0.4
        # Center the pipeline so token labels and final activation column both fit.
        x_embed = -(N_LAYERS * STAGE_DX) / 2 - 0.6

        # ---------- 1. Tokenize ----------
        # Sentence appears centered, as 3 Text pieces laid out side-by-side.
        sentence = VGroup(*[
            Text(t, font="Menlo", font_size=34, color=S.FG) for t in TOKENS
        ]).arrange(RIGHT, buff=0.3).move_to([0, 0, 0])
        self.play(FadeIn(sentence), run_time=S.BEAT)
        self.beat("BEAT")

        cap1 = self.show_caption("input is split into tokens, each becomes a vector")

        # Cut up: each word slides to its embedding-row's left side, scaling down.
        target_scale = 20 / 34
        token_anims = []
        for k, word in enumerate(sentence):
            target = [x_embed - 2.1, _row_y(k, cy), 0]
            token_anims.append(word.animate.move_to(target).scale(target_scale))
        self.play(*token_anims, run_time=S.HOLD)
        token_boxes = sentence  # alias for downstream code

        # ---------- 2. Embeddings (one row per token) ----------
        embed_vals = [rng.uniform(-1, 1, VEC_DIM) for _ in TOKENS]
        embeds = VGroup()
        embed_arrows = VGroup()
        for k, vals in enumerate(embed_vals):
            y = _row_y(k, cy)
            row = _vector_row(vals, (x_embed, y))
            embeds.add(row)
            embed_arrows.add(Arrow(
                token_boxes[k].get_right() + 0.05 * RIGHT,
                row.get_left() + 0.02 * LEFT,
                color=S.FG_DIM, stroke_width=2, buff=0.05,
            ))
        embed_lbl = Text("embeddings", font=S.FONT, font_size=15, color=S.FG_DIM)
        embed_lbl.next_to(embeds, DOWN, buff=0.18)
        self.play(GrowArrow(embed_arrows[0]), GrowArrow(embed_arrows[1]),
                  GrowArrow(embed_arrows[2]), run_time=S.QUICK)
        self.play(FadeIn(embeds, lag_ratio=0.05), Write(embed_lbl), run_time=S.BEAT)
        self.beat("BEAT")
        self.hide_caption(cap1)

        # ---------- 3. Layers ----------
        cap2 = self.show_caption("each layer updates every token's vector — the residual stream")

        block_h = max(
            (len(TOKENS) - 1) * (V_CELL_H + ROW_GAP) + V_CELL_H + 0.4,
            M_ROWS * M_CELL + 0.4,
        )

        prev_vals = embed_vals
        prev_rows = embeds
        keep: list = []

        for L in range(N_LAYERS):
            layer_x = x_embed + (L + 0.5) * STAGE_DX
            next_x = x_embed + (L + 1) * STAGE_DX

            layer = _layer_block(layer_x, cy, block_h)
            layer_lbl = Text(f"layer {L + 1}", font=S.FONT, font_size=15, color=S.FG_DIM)
            layer_lbl.next_to(layer, UP, buff=0.12)

            in_arrows = VGroup(*[
                Arrow(prev_rows[k].get_right() + 0.02 * RIGHT,
                      layer[0].get_left() + 0.02 * LEFT,
                      color=S.FG_DIM, stroke_width=1.8, buff=0.05)
                for k in range(len(TOKENS))
            ])

            self.play(FadeIn(layer), Write(layer_lbl),
                      *[GrowArrow(a) for a in in_arrows], run_time=S.BEAT)
            self.play(Indicate(prev_rows, color=S.HIGHLIGHT, scale_factor=1.04), run_time=S.BEAT)

            hot = rng.choice(M_ROWS * M_COLS, size=8, replace=False)
            self.play(AnimationGroup(
                *[Indicate(layer[1][i], color=S.STRUCTURE, scale_factor=1.5) for i in hot],
                lag_ratio=0.14,
            ), run_time=1.5)

            new_vals = [np.clip(v + rng.normal(0, 0.25, VEC_DIM), -0.99, 0.99) for v in prev_vals]
            new_rows = VGroup()
            out_arrows = VGroup()
            is_last_layer = (L == N_LAYERS - 1)
            for k in range(len(TOKENS)):
                y = _row_y(k, cy)
                color = S.HIGHLIGHT if (is_last_layer and k == len(TOKENS) - 1) else S.STRUCTURE
                placeholder = rng.uniform(-1, 1, VEC_DIM)
                row = _vector_row(placeholder, (next_x, y), color=color)
                new_rows.add(row)
                out_arrows.add(Arrow(layer[0].get_right() + 0.02 * RIGHT,
                                     row.get_left() + 0.02 * LEFT,
                                     color=S.FG_DIM, stroke_width=1.8, buff=0.05))

            self.play(*[GrowArrow(a) for a in out_arrows], run_time=S.BEAT)
            self.play(FadeIn(new_rows, lag_ratio=0.08), run_time=S.BEAT)

            # Cycle the numbers through random values, then settle on the real ones.
            for _ in range(3):
                cyc_anims = []
                for row in new_rows:
                    rand_vals = rng.uniform(-1, 1, VEC_DIM)
                    for j, cell in enumerate(row):
                        nxt = Text(_fmt(rand_vals[j]), font="Menlo",
                                   font_size=14, color=S.FG).move_to(cell[1])
                        cyc_anims.append(Transform(cell[1], nxt))
                self.play(*cyc_anims, run_time=0.18)

            settle_anims = []
            for k, row in enumerate(new_rows):
                for j, cell in enumerate(row):
                    nxt = Text(_fmt(new_vals[k][j]), font="Menlo",
                               font_size=14, color=S.FG).move_to(cell[1])
                    settle_anims.append(Transform(cell[1], nxt))
            self.play(*settle_anims, run_time=S.HOLD)
            self.beat("HOLD")

            keep.extend([layer, layer_lbl, in_arrows, out_arrows, new_rows])
            prev_vals = new_vals
            prev_rows = new_rows

        self.beat("BEAT")
        self.hide_caption(cap2)

        # ---------- 3a. One more pass: drop embeds + layer 1, run layer 2 ----------
        cap_again = self.show_caption("the next layer does the same thing again")

        first_layer = keep[0]
        first_layer_lbl = keep[1]
        first_in_arrows = keep[2]
        first_out_arrows = keep[3]
        self.play(
            FadeOut(embeds), FadeOut(embed_arrows), FadeOut(embed_lbl),
            FadeOut(first_layer), FadeOut(first_layer_lbl),
            FadeOut(first_in_arrows), FadeOut(first_out_arrows),
            run_time=S.BEAT,
        )

        # Slide post-layer-1 activations (and tokens) left into the embedding slot.
        acts_layer1 = prev_rows
        self.play(
            acts_layer1.animate.shift(LEFT * STAGE_DX),
            token_boxes.animate.shift(LEFT * STAGE_DX),
            run_time=S.HOLD,
        )

        # Layer 2 at the position layer 1 used to occupy.
        layer2_x = x_embed + 0.5 * STAGE_DX
        out2_x = x_embed + 1.0 * STAGE_DX

        layer2 = _layer_block(layer2_x, cy, block_h)
        layer2_lbl = Text("layer 2", font=S.FONT, font_size=15, color=S.FG_DIM)
        layer2_lbl.next_to(layer2, UP, buff=0.12)

        in2_arrows = VGroup(*[
            Arrow(acts_layer1[k].get_right() + 0.02 * RIGHT,
                  layer2[0].get_left() + 0.02 * LEFT,
                  color=S.FG_DIM, stroke_width=1.8, buff=0.05)
            for k in range(len(TOKENS))
        ])

        self.play(FadeIn(layer2), Write(layer2_lbl),
                  *[GrowArrow(a) for a in in2_arrows], run_time=S.BEAT)
        self.play(Indicate(acts_layer1, color=S.HIGHLIGHT, scale_factor=1.04), run_time=S.BEAT)

        hot2 = rng.choice(M_ROWS * M_COLS, size=8, replace=False)
        self.play(AnimationGroup(
            *[Indicate(layer2[1][i], color=S.STRUCTURE, scale_factor=1.5) for i in hot2],
            lag_ratio=0.14,
        ), run_time=1.2)

        new_vals2 = [np.clip(v + rng.normal(0, 0.25, VEC_DIM), -0.99, 0.99) for v in prev_vals]
        new_rows2 = VGroup()
        out2_arrows = VGroup()
        for k in range(len(TOKENS)):
            y = _row_y(k, cy)
            color = S.HIGHLIGHT if k == len(TOKENS) - 1 else S.STRUCTURE
            placeholder = rng.uniform(-1, 1, VEC_DIM)
            row = _vector_row(placeholder, (out2_x, y), color=color)
            new_rows2.add(row)
            out2_arrows.add(Arrow(layer2[0].get_right() + 0.02 * RIGHT,
                                  row.get_left() + 0.02 * LEFT,
                                  color=S.FG_DIM, stroke_width=1.8, buff=0.05))

        self.play(*[GrowArrow(a) for a in out2_arrows], run_time=S.BEAT)
        self.play(FadeIn(new_rows2, lag_ratio=0.08), run_time=S.BEAT)

        settle2 = []
        for k, row in enumerate(new_rows2):
            for j, cell in enumerate(row):
                nxt = Text(_fmt(new_vals2[k][j]), font="Menlo",
                           font_size=14, color=S.FG).move_to(cell[1])
                settle2.append(Transform(cell[1], nxt))
        self.play(*settle2, run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap_again)

        prev_rows = new_rows2
        prev_vals = new_vals2
        layer = layer2  # the "× many layers" stack builds behind this one
        keep.append(layer2)

        # ---------- 3b. "× many layers" stack ----------
        cap_many = self.show_caption("in real models, this happens across many layers")
        self.beat("HOLD")

        # Clear everything except layer2 (kept for the stack) and the final
        # activation row on the right.
        non_final_rows2 = VGroup(*[r for k, r in enumerate(new_rows2) if k != len(TOKENS) - 1])
        self.play(
            FadeOut(token_boxes),
            FadeOut(acts_layer1),
            FadeOut(in2_arrows), FadeOut(out2_arrows),
            FadeOut(layer2_lbl),
            FadeOut(non_final_rows2),
            run_time=S.HOLD,
        )
        self.beat("BEAT")

        # Stack ghost copies of the layer behind the main one (perspective-ish).
        stack_copies = VGroup()
        for i in range(5):
            o = i + 1
            ghost = layer[0].copy()
            ghost.set_stroke(color=S.STRUCTURE, width=1.4, opacity=max(0.55 - o * 0.09, 0.1))
            ghost.set_fill(color=S.STRUCTURE, opacity=max(0.05 - o * 0.008, 0.0))
            ghost.shift(np.array([0.22, 0.18, 0]) * o)
            ghost.set_z_index(-o)
            stack_copies.add(ghost)
        layer.set_z_index(1)

        many_lbl = Text("× many layers", font=S.FONT, font_size=22, color=S.FG_DIM)
        many_lbl.next_to(layer, DOWN, buff=0.5)

        self.play(FadeIn(stack_copies, lag_ratio=0.32), run_time=2.2)
        self.play(FadeIn(many_lbl), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap_many)

        # ---------- 4. Isolate last token's final activation ----------
        cap3 = self.show_caption("the last token's final activation predicts the next word")
        final_row = prev_rows[-1]
        # Only fade what's still on screen: the stack, the label, and layer 2.
        # (Earlier embeddings / arrows / layer 1 were already faded out.)
        still_on_screen = VGroup(stack_copies, many_lbl, layer)
        self.play(FadeOut(still_on_screen), run_time=S.BEAT)
        self.play(final_row.animate.move_to([-4.3, 0, 0]).scale(1.3), run_time=S.HOLD)

        # ---------- 5. Unembed → logits → predicted token ----------
        # W_U: tall matrix to the right. Vocab = 6 candidate next words.
        VOCAB = ["delicious", "sour", "crunchy", "with", "on", "bad"]
        wu_x = -0.4
        wu_cell = 0.32
        wu_cols = VEC_DIM
        wu_rows = len(VOCAB)
        wu_grid = VGroup()
        wu_top = (wu_rows - 1) * wu_cell / 2
        wu_left = wu_x - (wu_cols - 1) * wu_cell / 2
        for i in range(wu_rows):
            for j in range(wu_cols):
                wu_grid.add(Rectangle(
                    width=wu_cell, height=wu_cell,
                    stroke_color=S.STRUCTURE, stroke_width=0.7,
                    fill_color=S.STRUCTURE,
                    fill_opacity=float(rng.uniform(0.08, 0.35)),
                ).move_to([wu_left + j * wu_cell, wu_top - i * wu_cell, 0]))
        wu_lbl = Text("W_U   (unembedding)", font=S.FONT, font_size=15, color=S.STRUCTURE)
        wu_lbl.next_to(wu_grid, UP, buff=0.15)

        times = Text("×", font=S.FONT, font_size=28, color=S.FG_DIM).move_to([-2.0, 0, 0])
        equals = Text("=", font=S.FONT, font_size=28, color=S.FG_DIM).move_to([0.7, 0, 0])

        self.play(FadeIn(times), run_time=S.BEAT)
        self.play(FadeIn(wu_grid, lag_ratio=0.005), Write(wu_lbl), run_time=S.HOLD)
        self.play(FadeIn(equals), run_time=S.BEAT)

        # Logits: simulate as random scores, with "delicious" winning.
        logits = rng.uniform(-1.5, 1.5, len(VOCAB))
        logits[0] = 3.2  # "delicious" wins
        # Softmax
        probs = np.exp(logits - logits.max())
        probs /= probs.sum()

        bar_x = 3.0
        bar_max = 2.0
        word_x = bar_x - 0.2
        logit_rows = VGroup()
        for i, (w, p) in enumerate(zip(VOCAB, probs)):
            y = wu_top - i * wu_cell
            label = Text(w, font="Menlo", font_size=16, color=S.FG).move_to([word_x, y, 0])
            label.align_to([word_x, 0, 0], RIGHT)
            bar_w = max(float(p) * bar_max, 0.06)
            is_top = (i == 0)
            bar = Rectangle(
                width=bar_w, height=wu_cell * 0.8,
                stroke_width=0,
                fill_color=S.STRUCTURE if is_top else S.DATA,
                fill_opacity=0.95 if is_top else 0.5,
            )
            bar.move_to([bar_x + bar_w / 2, y, 0])
            logit_rows.add(VGroup(label, bar))
        logits_lbl = Text("next-token probabilities", font=S.FONT, font_size=15, color=S.FG_DIM)
        logits_lbl.next_to(logit_rows, UP, buff=0.15)

        self.play(FadeIn(logit_rows, lag_ratio=0.12), Write(logits_lbl), run_time=1.6)
        self.beat("HOLD")
        self.hide_caption(cap3)

        # Highlight prediction.
        cap4 = self.show_caption('predicted next token: "delicious"')
        self.play(Indicate(logit_rows[0], color=S.STRUCTURE, scale_factor=1.15), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap4)

        all_objs = VGroup(final_row, times, equals, wu_grid, wu_lbl, logit_rows, logits_lbl)
        self.play(FadeOut(all_objs), run_time=S.BEAT)
