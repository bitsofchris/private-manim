"""A batched matrix multiply applies the same linear map to every input row.

Viewer takeaway: each row of X supplies weights for the rows of W, producing
one output row; PyTorch does this for the whole batch at once.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql batched_linear_map_tensors.py BatchedLinearMapTensors
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene


X_ROWS = [
    ["1.0", "2.0", "-1.0"],
    ["0.0", "-1.0", "3.0"],
    ["2.0", "0.5", "1.0"],
    ["-1.0", "1.0", "2.0"],
    ["3.0", "-2.0", "0.0"],
]
W_ROWS = [["2.0", "-1.0"], ["0.5", "1.0"], ["-1.0", "2.0"]]
Y_ROWS = [["4.1", "-1.2"], ["-3.4", "4.8"], ["3.35", "0.3"], ["-3.4", "5.8"], ["5.1", "-5.2"]]
ROW_COLORS = [S.DATA, S.STRUCTURE, S.CONTENT_GOLD]


def txt(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


class TensorTable(VGroup):
    def __init__(self, name: str, shape: str, rows: list[list[str]], cell_w: float, cell_h: float):
        super().__init__()
        self.cells: list[list[VGroup]] = []
        self.name = txt(f"{name}: tensor", S.FG)
        self.shape = txt(shape, S.FG_DIM, scale=S.TAG_SCALE)
        body = VGroup()
        for r, row in enumerate(rows):
            rendered_row = []
            for c, value in enumerate(row):
                box = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    stroke_color=S.MUTED,
                    stroke_width=S.STROKE_AXIS,
                    fill_color=S.BG_PANEL,
                    fill_opacity=S.OP_GHOST,
                )
                value_text = txt(value, S.FG_DIM, scale=S.TAG_SCALE).move_to(box)
                cell = VGroup(box, value_text)
                cell.move_to(RIGHT * c * cell_w + DOWN * r * cell_h)
                rendered_row.append(cell)
                body.add(cell)
            self.cells.append(rendered_row)
        self.body = body
        header = VGroup(self.name, self.shape).arrange(DOWN, buff=0.08)
        self.add(header, body)
        self.arrange(DOWN, buff=0.22)

    def row_group(self, index: int) -> VGroup:
        return VGroup(*self.cells[index])

    def color_row(self, index: int, color: str) -> AnimationGroup:
        anims = []
        for cell in self.cells[index]:
            anims.append(cell[0].animate.set_stroke(color=color, width=S.STROKE_STRUCTURE))
            anims.append(cell[1].animate.set_color(color))
        return AnimationGroup(*anims)

    def reset_rows(self) -> AnimationGroup:
        anims = []
        for row in self.cells:
            for cell in row:
                anims.append(cell[0].animate.set_stroke(color=S.MUTED, width=S.STROKE_AXIS))
                anims.append(cell[1].animate.set_color(S.FG_DIM))
        return AnimationGroup(*anims)


class BatchedLinearMapTensors(BocScene):
    def construct(self):
        title = txt("Y = X @ W + b", S.FG).to_corner(UL, buff=0.28)
        x_table = TensorTable("X", "shape (5, 3)", X_ROWS, 0.62, 0.42).to_edge(LEFT, buff=0.55).shift(DOWN * 0.2)
        w_table = TensorTable("W", "shape (3, 2)", W_ROWS, 0.68, 0.42).move_to(ORIGIN).shift(DOWN * 0.2)
        y_table = TensorTable("Y", "shape (5, 2)", Y_ROWS, 0.72, 0.42).to_edge(RIGHT, buff=0.55).shift(DOWN * 0.2)
        b_vec = TensorTable("b", "shape (2,)", [["0.1", "-0.2"]], 0.72, 0.42).next_to(y_table, DOWN, buff=0.34)
        op = txt("@", S.STRUCTURE, scale=S.CAPTION_SCALE).move_to((x_table.get_right() + w_table.get_left()) / 2)
        plus = txt("+", S.STRUCTURE, scale=S.CAPTION_SCALE).move_to((w_table.get_right() + y_table.get_left()) / 2 + DOWN * 1.35)

        self.play(FadeIn(title), run_time=S.BEAT)
        cap = self.show_caption("Five 3D rows go through the same 3D to 2D map.")
        self.play(FadeIn(x_table), FadeIn(op), FadeIn(w_table), run_time=S.HOLD)
        self.play(FadeIn(plus), FadeIn(b_vec), FadeIn(y_table), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        self.explain_one_row(x_table, w_table, y_table)
        self.sweep_batch(x_table, w_table, y_table)
        self.show_shape_check(title, x_table, w_table, y_table, b_vec, op, plus)

    def explain_one_row(self, x_table: TensorTable, w_table: TensorTable, y_table: TensorTable) -> None:
        cap = self.show_caption("One row of X gives the three weights.")
        weighted_rows = VGroup()
        for i, color in enumerate(ROW_COLORS):
            weighted_rows.add(txt(f"{X_ROWS[0][i]} * W row {i + 1}", color))
        weighted_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(w_table, DOWN, buff=0.42)

        self.play(x_table.color_row(0, S.DATA), run_time=S.BEAT)
        for i, color in enumerate(ROW_COLORS):
            self.play(w_table.color_row(i, color), FadeIn(weighted_rows[i]), run_time=S.BEAT)
            self.beat("QUICK")

        result = txt("sum -> Y row 1", S.STRUCTURE).next_to(y_table, UP, buff=0.2)
        self.play(y_table.color_row(0, S.STRUCTURE), FadeIn(result), run_time=S.BEAT)
        self.beat("HOLD")
        self.play(FadeOut(weighted_rows), FadeOut(result), w_table.reset_rows(), run_time=S.BEAT)
        self.hide_caption(cap)

    def sweep_batch(self, x_table: TensorTable, w_table: TensorTable, y_table: TensorTable) -> None:
        cap = self.show_caption("PyTorch runs that same pairing for every row in parallel.")
        all_w = AnimationGroup(*[w_table.color_row(i, ROW_COLORS[i]) for i in range(3)])
        self.play(all_w, run_time=S.BEAT)
        for r in range(5):
            self.play(x_table.reset_rows(), y_table.reset_rows(), run_time=S.QUICK)
            self.play(x_table.color_row(r, S.DATA), y_table.color_row(r, S.STRUCTURE), run_time=S.BEAT)
        self.beat("HOLD")
        self.play(x_table.reset_rows(), y_table.reset_rows(), w_table.reset_rows(), run_time=S.BEAT)
        self.hide_caption(cap)

    def show_shape_check(
        self,
        title: Text,
        x_table: TensorTable,
        w_table: TensorTable,
        y_table: TensorTable,
        b_vec: TensorTable,
        op: Text,
        plus: Text,
    ) -> None:
        self.play(
            FadeOut(x_table),
            FadeOut(w_table),
            FadeOut(y_table),
            FadeOut(b_vec),
            FadeOut(title),
            FadeOut(op),
            FadeOut(plus),
            run_time=S.BEAT,
        )
        checks = VGroup(
            txt("X is (5, 3)", S.DATA),
            txt("W is (3, 2)", S.STRUCTURE),
            txt("X @ W is (5, 2)", S.FG),
            txt("b is (2,), broadcast across rows", S.CONTENT_GOLD),
            txt("Y is (5, 2)", S.FG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(ORIGIN)
        code = txt("torch.randn(5, 3) @ W + b", S.FG_DIM).next_to(checks, DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(row) for row in checks], lag_ratio=0.16), run_time=S.HOLD)
        self.play(FadeIn(code), run_time=S.BEAT)
        self.beat("HOLD")
