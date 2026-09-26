"""Beat 6 (8.56 s): the gradient is a list of directions, one per parameter.

VO (scene-local): "gives us what's called the gradient," 0.0-3.0 ("gradient"
~2.3); "which is just a list of changes" 3.0-4.6; "to all the parameters in
our network" 4.6-6.1; "that tell us which direction to nudge them all."
6.1-8.56 ("direction" ~6.9).
Opens on beat 5's last frame (same graph, every grad filled). The leaves'
grads lift out into a bracketed column on a card at the right of the stage;
the nodes the card covers (x, b, L, the ops and every edge) fade out fully so
nothing shows through or pokes out; w and a stay, ghosted, on the left.
Magenta hero: the assembled gradient (values, label, arrows).

Render:
    cd videos/004-backprop-short && uv run --no-sync manim -qh 06_gradient.py Gradient
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # local _graph module

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import hero_arrow
from _graph import NODES, PARAMS, build_graph, txt

DURATION = 8.56
T_GRADIENT = 2.0      # "the gradient" (lift lands through ~3.2)
T_LIST = 3.4          # "a list of changes"
T_PARAMS = 4.8        # "all the parameters"
T_DIRECTION = 6.9     # "which direction to nudge"
KEEP = ("w", "a")     # nodes left of the card: stay, ghosted
N_MORE = 3            # placeholder rows: every other weight in a network
ROW_PITCH = 1.1
CARD_PAD = 0.3
BRACKET_LIP = 0.18
ARROW_LEN = 0.75
MORE_DIRS = [DOWN, UP, DOWN]  # placeholder arrows (dim): each weight has its own


def bracket(top: float, bottom: float, x: float, side) -> VMobject:
    """A square bracket from top to bottom at x; side=LEFT opens right."""
    lip = -side[0] * BRACKET_LIP
    return VMobject(stroke_color=S.FG, stroke_width=S.STROKE_STRUCTURE).set_points_as_corners(
        [[x + lip, top, 0], [x, top, 0], [x, bottom, 0], [x + lip, bottom, 0]])


class Gradient(BocShortScene):
    def construct(self):
        g = build_graph(self.stage, final=True)
        self.add(g)
        values = [g.nodes[k].grad[4:] for k in PARAMS]   # "grad 3.0" -> "3.0"

        # Layout of the column: header, 2 value rows, N_MORE placeholder rows.
        header = txt("gradient", S.STRUCTURE, "BOLD")
        rows = [txt(NODES[k][1], S.STRUCTURE) for k in PARAMS]
        more = [txt("…", S.FG_DIM) for _ in range(N_MORE)]
        tags = [txt(k, S.FG_DIM) for k in PARAMS]
        n_all = len(rows) + N_MORE
        card_h = header.height + ROW_PITCH * n_all + 3 * CARD_PAD
        card_w = self.stage.width * 0.52
        card = RoundedRectangle(corner_radius=0.2, width=card_w, height=card_h,
                                fill_color=S.BG_PANEL, fill_opacity=1,
                                stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS)
        card.align_to(self.stage, UP + RIGHT)
        header.next_to(card.get_top(), DOWN, buff=CARD_PAD)
        col_x = card.get_x() - 0.1
        row_y = [header.get_bottom()[1] - CARD_PAD - ROW_PITCH * (i + 0.5) for i in range(n_all)]
        for m, y in zip(rows + more, row_y):
            m.move_to([col_x, y, 0])
        half = rows[0].width / 2 + 0.35
        lx, rx = col_x - half, col_x + half
        top = row_y[0] + ROW_PITCH / 2

        def brackets(n: int) -> VGroup:
            bottom = row_y[n - 1] - ROW_PITCH / 2
            return VGroup(bracket(top, bottom, lx, LEFT), bracket(top, bottom, rx, RIGHT))

        br = brackets(len(rows))
        for t, r in zip(tags, rows):
            t.next_to([lx, r.get_y(), 0], LEFT, buff=0.2)
        arrow_x = rx + 0.45

        def arrow(y: float, d, color) -> Arrow:
            return hero_arrow([arrow_x, y - d[1] * ARROW_LEN / 2, 0],
                              [arrow_x, y + d[1] * ARROW_LEN / 2, 0], color=color,
                              max_stroke_width_to_length_ratio=20, max_tip_length_to_length_ratio=0.4)

        # "the gradient": the leaves' grads lift out into a list; the graph recedes.
        self.hold_until(T_GRADIENT)
        # Card, header and brackets are pre-added invisible so the lifted values
        # (added by the play) layer above the card.
        card.set_opacity(0), header.set_opacity(0), br.set_stroke(opacity=0)
        self.add(card, header, br)
        recede = [g.nodes[k].animate.set_opacity(S.OP_GHOST) for k in KEEP]
        hide = [m.animate.set_opacity(0) for m in g if all(m is not g.nodes[k] for k in KEEP)]
        self.play(*recede, *hide, card.animate.set_opacity(1),
                  header.animate.set_opacity(1), br.animate.set_stroke(opacity=1),
                  *[TransformFromCopy(v, r) for v, r in zip(values, rows)], run_time=S.HOLD)

        # "a list of changes to all the parameters": one entry per weight.
        self.hold_until(T_LIST)
        self.play(Transform(br, brackets(n_all)), FadeIn(VGroup(*more), lag_ratio=0.3),
                  run_time=S.HOLD)
        self.hold_until(T_PARAMS)
        self.play(FadeIn(VGroup(*tags)), run_time=S.BEAT)

        # "which direction to nudge them all": every entry is a direction.
        self.hold_until(T_DIRECTION)
        arrows = VGroup(*[arrow(r.get_y(), UP, S.STRUCTURE) for r in rows],
                        *[arrow(m.get_y(), d, S.FG_DIM) for m, d in zip(more, MORE_DIRS)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=S.HOLD)
        self.hold_until(DURATION)
