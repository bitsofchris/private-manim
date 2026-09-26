"""backward() seeds dL/dL = 1 at the loss, then walks the graph back via the chain rule.

Render:
    cd videos/003-backprop-gifs && uv run manim -qm 04_backprop_graph.py BackpropGraph
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocScene

# name: (data, final grad, grid position (col, row))
NODES = {
    "w": ("2.0", "3.0", (0, 1.0)),
    "x": ("3.0", "2.0", (0, -1.0)),
    "a": ("6.0", "1.0", (2, 0.0)),
    "b": ("1.0", "1.0", (2, -2.0)),
    "L": ("7.0", "1.0", (4, -1.0)),
}
OPS = {"*": (1, 0.0), "+": (3, -1.0)}
EDGES = [("w", "*"), ("x", "*"), ("*", "a"), ("a", "+"), ("b", "+"), ("+", "L")]
COL_W, ROW_H = 2.15, 1.25
GRAPH_SCALE = 1.18  # fill the frame; text must stay legible at 640px


def txt(s: str, color: str = S.FG, weight: str = "NORMAL") -> Text:
    return Text(s, font=S.FONT, weight=weight).scale(S.CAPTION_SCALE).set_color(color)


def grid(col: float, row: float) -> np.ndarray:
    return np.array([col * COL_W, row * ROW_H, 0.0])


def value_node(name: str, data: str) -> VGroup:
    lines = VGroup(
        txt(name, S.FG, "BOLD"),
        txt(f"data {data}", S.DATA),
        txt("grad ?", S.FG_DIM),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    box = RoundedRectangle(
        corner_radius=0.15, width=lines.width + 0.45, height=lines.height + 0.35,
        stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS,
        fill_color=S.BG_PANEL, fill_opacity=1,
    )
    lines.move_to(box)
    return VGroup(box, lines)


def op_node(sym: str) -> VGroup:
    c = Circle(radius=0.36, stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS,
               fill_color=S.BG_PANEL, fill_opacity=1)
    return VGroup(c, txt(sym, S.FG, "BOLD").move_to(c))


class BackpropGraph(BocScene):
    def construct(self):
        nodes = {k: value_node(k, d).move_to(grid(*p)) for k, (d, _, p) in NODES.items()}
        nodes.update({k: op_node(k).move_to(grid(*p)) for k, p in OPS.items()})
        edges = {
            (u, v): Arrow(nodes[u].get_right(), nodes[v].get_left(), buff=0.08,
                          color=S.MUTED, stroke_width=S.STROKE_AXIS * 2,
                          max_tip_length_to_length_ratio=0.2)
            for u, v in EDGES
        }
        graph = VGroup(*edges.values(), *nodes.values())
        graph.scale(GRAPH_SCALE).move_to(DOWN * 0.35)
        self.add(graph)
        self.nodes = nodes

        # Beat 1: the forward pass left a graph behind.
        cap = self.show_caption("forward pass stored the graph")
        self.beat("HOLD")
        self.hide_caption(cap)

        # Beat 2: seed the loss.
        cap = self.show_caption("start: dL/dL = 1")
        self.play(self.fill("L"), run_time=S.BEAT)
        self.play(Indicate(self.grad("L"), color=S.CALLOUT, scale_factor=1.25), run_time=S.BEAT)
        self.hide_caption(cap)

        # Beat 3: walk back through +, then through *.
        cap = self.show_caption("walk back, chain rule")
        self.play(self.flow(edges, [("+", "L"), ("a", "+"), ("b", "+")]),
                  self.settle("L"), run_time=S.BEAT)
        self.play(self.fill("a"), self.fill("b"), run_time=S.BEAT)
        self.play(self.flow(edges, [("*", "a"), ("w", "*"), ("x", "*")]),
                  self.settle("a"), self.settle("b"), run_time=S.BEAT)
        mw = self.product("1.0 × 3.0").next_to(nodes["w"], UP, buff=0.15)
        mx = self.product("1.0 × 2.0").next_to(nodes["x"], DOWN, buff=0.15)
        self.play(FadeIn(mw, shift=DOWN * 0.2), FadeIn(mx, shift=UP * 0.2),
                  self.fill("w"), self.fill("x"), run_time=S.BEAT)
        self.beat("BEAT")
        self.play(FadeOut(mw), FadeOut(mx), run_time=S.QUICK)
        self.hide_caption(cap)
        self.beat("HOLD")

    def grad(self, name: str) -> Text:
        return self.nodes[name][1][2]

    def fill(self, name: str) -> Animation:
        old = self.grad(name)
        new = txt(f"grad {NODES[name][1]}", S.STRUCTURE).move_to(old, aligned_edge=LEFT)
        return Transform(old, new)

    def settle(self, name: str) -> Animation:
        return self.grad(name).animate.set_color(S.FG)

    def flow(self, edges: dict, keys: list) -> AnimationGroup:
        # Backward pulse: magenta flash travelling from each edge's head to its tail.
        flashes = [
            ShowPassingFlash(
                Line(edges[k].get_end(), edges[k].get_start(),
                     color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE * 1.6),
                time_width=0.6,
            )
            for k in keys
        ]
        return AnimationGroup(*flashes)

    def product(self, s: str) -> Text:
        return txt(s, S.CALLOUT, "BOLD")
