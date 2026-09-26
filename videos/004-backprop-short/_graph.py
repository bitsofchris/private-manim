"""Vertical micrograd-style graph shared by beats 5 (backprop) and 6 (gradient).

Leaves w, x at the top of the stage, `*`, then a and b, `+`, and the loss L at
the bottom. Value nodes are rounded boxes with a "data" line (teal) and a
"grad" line; the node name sits just above the box's outer top corner.
Numbers match videos/003-backprop-gifs/04_backprop_graph.py.

    g = build_graph(self.stage)              # every grad "?"  (beat 5 start)
    g = build_graph(self.stage, final=True)  # all grads filled (beat 5 end = beat 6 start)
"""
from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, Line, RoundedRectangle, Text, VGroup, np,
)

from videos._shared import style as S

# name: (data, final grad, column: -1 left / +1 right / 0 centre, row 0..2)
NODES = {
    "w": ("2.0", "3.0", -1, 0),
    "x": ("3.0", "2.0", +1, 0),
    "a": ("6.0", "1.0", -1, 1),
    "b": ("1.0", "1.0", +1, 1),
    "L": ("7.0", "1.0", 0, 2),
}
OPS = {"*": 0.5, "+": 1.5}   # op symbol -> row (sits in the gap between rows)
OP_GLYPH = {"*": "×", "+": "+"}
EDGES = [("w", "*"), ("x", "*"), ("*", "a"), ("a", "+"), ("b", "+"), ("+", "L")]
PARAMS = ("w", "x")          # the leaves a network would learn

LINE_BUFF = 0.08             # between the data and grad lines
BOX_PAD = 0.1                # text-to-border padding
OP_RADIUS = 0.3
NAME_BUFF = 0.06
EDGE_WIDTH = S.STROKE_AXIS * 3
WIDEST = "grad 3.0"          # widest line; boxes hug it, the column gap takes the rest


def txt(s: str, color: str = S.FG, weight: str = "NORMAL") -> Text:
    return Text(s, font=S.FONT, weight=weight).scale(S.SHORT_LABEL_SCALE).set_color(color)


def grad_text(value: str, color: str) -> Text:
    return txt(f"grad {value}", color)


class ValueNode(VGroup):
    """Box + name tab + data line + grad line. `.grad` is the grad Text."""

    def __init__(self, name: str, data: str, grad: str, grad_color: str, width: float,
                 tab_side):
        super().__init__()
        self.data = txt(f"data {data}", S.DATA)
        # Layout uses a fixed reference slot, so every node has the same box
        # whatever its grad says (beat 5's last frame == beat 6's first frame).
        self.slot = grad_text("0.0", grad_color)
        lines = VGroup(self.data, self.slot).arrange(DOWN, aligned_edge=LEFT, buff=LINE_BUFF)
        self.box = RoundedRectangle(
            corner_radius=0.18, width=width, height=lines.height + 2 * BOX_PAD,
            stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 1.5,
            fill_color=S.BG_PANEL, fill_opacity=1,
        )
        lines.move_to(self.box).align_to(self.box, LEFT).shift(RIGHT * BOX_PAD * 1.5)
        # Slot geometry relative to the box (the reference Text is not added).
        self._slot_dl = self.slot.get_corner(DOWN + LEFT) - self.box.get_center()
        self._slot_mid = self.slot[4:].get_center() - self.box.get_center()
        self.name = txt(name, S.FG, "BOLD")
        self.name.set_stroke(S.BG_DEEP, width=12, background=True)
        # Name sits just above the box's outer top corner (never over the text).
        self.name.next_to(self.box, UP, buff=NAME_BUFF).align_to(self.box, tab_side)
        self.name.shift(-tab_side * BOX_PAD * 1.5)
        self.grad = self.place(grad_text(grad, grad_color))
        self.add(self.box, self.data, self.grad, self.name)

    def place(self, t: Text) -> Text:
        """Put `t` in the grad slot: "grad ..." shares the slot's baseline (every
        one has the g descender); anything else is centred on the slot's line."""
        c = self.box.get_center()
        if t.original_text.startswith("grad"):
            return t.move_to(c + self._slot_dl, aligned_edge=DOWN + LEFT)
        t.move_to(c + self._slot_dl, aligned_edge=LEFT)
        return t.set_y((c + self._slot_mid)[1])


def op_node(sym: str) -> VGroup:
    c = Circle(radius=OP_RADIUS, stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 1.5,
               fill_color=S.BG_PANEL, fill_opacity=1)
    return VGroup(c, txt(OP_GLYPH[sym], S.FG, "BOLD").move_to(c))


def build_graph(stage, final: bool = False) -> VGroup:
    """The graph filling `stage`. Attributes: .nodes (name -> mobject), .edges
    ((u, v) -> Line, drawn tail->head in the forward direction)."""
    box_w = txt(WIDEST).width + 2.5 * BOX_PAD
    half = (stage.width - box_w) / 2           # columns flush with the stage edges
    col_x = {-1: -half, +1: half, 0: 0.0}
    nodes = {}
    for name, (data, g, col, _) in NODES.items():
        filled = final
        color = S.STRUCTURE if final and name in PARAMS else S.FG
        tab = LEFT if col <= 0 else RIGHT
        nodes[name] = ValueNode(name, data, g if filled else "?",
                                color if filled else S.FG_DIM, box_w, tab)
    box_h = nodes["w"].box.height
    tab_over = nodes["w"].name.get_top()[1] - nodes["w"].box.get_top()[1]
    gap = (stage.height - tab_over - 3 * box_h) / 2
    pitch = box_h + gap
    top = stage.get_top()[1] - tab_over - box_h / 2
    for name, (_, _, col, row) in NODES.items():
        nodes[name].move_to([stage.get_x() + col_x[col], top - row * pitch, 0])
    for sym, row in OPS.items():
        nodes[sym] = op_node(sym).move_to([stage.get_x(), top - row * pitch, 0])

    def anchor(u, v):
        # Edge endpoints: a box's inner bottom/top corner region, an op's rim.
        nu, nv = nodes[u], nodes[v]
        if u in OPS:
            start = nu[0].point_at_angle(np.angle(complex(*(nv.get_center() - nu.get_center())[:2])))
        else:
            start = nu.box.get_bottom() + RIGHT * np.sign(nv.get_x() - nu.get_x()) * box_w * 0.4
        if v in OPS:
            end = nv[0].point_at_angle(np.angle(complex(*(nu.get_center() - nv.get_center())[:2])))
        else:
            end = nv.box.get_top() + RIGHT * np.sign(nu.get_x() - nv.get_x()) * box_w * 0.4
        return start, end

    edges = {(u, v): Line(*anchor(u, v), color=S.FG_DIM, stroke_width=EDGE_WIDTH,
                           stroke_opacity=S.OP_DATA) for u, v in EDGES}
    graph = VGroup(*edges.values(), *nodes.values())
    graph.nodes, graph.edges = nodes, edges
    return graph
