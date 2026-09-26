"""Beat 5 (12.61 s): backprop seeds grad 1 at the loss and walks the graph backwards.

VO (scene-local): "And backprop is when we start at the loss," 0.0-2.0;
"set the gradient there equal to 1," 2.0-4.2; "we then walk the computational
graph backwards" 4.2-6.7; "and then a rule from calculus called the chain rule"
6.7-9.2; "is what allows us to take these local derivatives," 9.2-11.0;
"getting the partial derivatives" 11.0-12.6.
Magenta hero: the gradient, one node's grad at a time, flowing up the graph.
The local derivatives ("1.0×3.0") appear in w's and x's grad slot itself:
there is no free space beside the leaves at phone-legible text size.

Render:
    cd videos/004-backprop-short && uv run --no-sync manim -qh 05_backprop.py Backprop
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # local _graph module

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from _graph import NODES, build_graph, grad_text, txt

DURATION = 13.97
T_LOSS = 0.0          # "start at the loss" (Indicate peaks ~0.6)
T_ONE = 3.0           # "equal to 1"
T_BACK = 4.4          # "walk the computational graph backwards"
T_CHAIN = 7.0         # "chain rule"
T_LOCAL = 9.3         # "local derivatives"
T_PARTIAL = 11.1      # "partial derivatives"
LOCAL = {"w": "1.0×3.0", "x": "1.0×2.0"}   # no spaces: must fit the grad slot
PULSE_RADIUS = 0.26   # the travelling gradient: a magenta dot (edges are too short to flash)


class Backprop(BocShortScene):
    def construct(self):
        g = build_graph(self.stage)
        self.g = g
        self.add(g)

        # "start at the loss": point at L's grad slot.
        self.play(Indicate(self.grad("L"), color=S.CALLOUT, scale_factor=1.15), run_time=S.HOLD)

        # "equal to 1": the seed.
        self.hold_until(T_ONE)
        self.play(self.fill("L"), run_time=S.BEAT)

        # "walk the computational graph backwards": up through + into a and b.
        self.hold_until(T_BACK)
        dot = self.pulse("L")
        self.play(FadeIn(dot, scale=0.3), self.travel(dot, "+"), run_time=S.BEAT)
        da, db = dot, dot.copy()
        self.play(self.travel(da, "a"), self.travel(db, "b"), run_time=S.BEAT)
        self.play(self.fill("a"), self.fill("b"), self.settle("L"),
                  FadeOut(da), FadeOut(db), run_time=S.BEAT)

        # "chain rule": the pulse keeps going, through * to the leaves.
        self.hold_until(T_CHAIN)
        dot = self.pulse("a")
        self.play(FadeIn(dot, scale=0.3), self.travel(dot, "*"), self.settle("a"),
                  self.settle("b"), run_time=S.BEAT)
        dw, dx = dot, dot.copy()
        self.play(self.travel(dw, "w"), self.travel(dx, "x"), run_time=S.BEAT)
        self.play(FadeOut(dw), FadeOut(dx), run_time=S.QUICK)

        # "local derivatives": upstream grad × the other input, in the grad slot.
        self.hold_until(T_LOCAL)
        self.play(*[self.swap(k, txt(s, S.CALLOUT)) for k, s in LOCAL.items()],
                  run_time=S.BEAT)

        # "partial derivatives": they resolve to w's and x's gradients.
        self.hold_until(T_PARTIAL)
        self.play(*[self.swap(k, grad_text(NODES[k][1], S.STRUCTURE)) for k in LOCAL],
                  run_time=S.BEAT)
        self.hold_until(DURATION)

    def grad(self, name: str) -> Text:
        return self.g.nodes[name].grad

    def swap(self, name: str, new: Text) -> Animation:
        """Replace a node's grad slot text: old lifts out, new lifts in."""
        node = self.g.nodes[name]
        node.place(new)
        anim = AnimationGroup(FadeOut(node.grad, shift=UP * 0.15),
                              FadeIn(new, shift=UP * 0.15), lag_ratio=0.4)
        node.grad = new
        return anim

    def fill(self, name: str) -> Animation:
        return self.swap(name, grad_text(NODES[name][1], S.STRUCTURE))

    def settle(self, name: str) -> Animation:
        return self.grad(name).animate.set_color(S.FG)

    def at(self, name: str) -> np.ndarray:
        n = self.g.nodes[name]
        return n.grad.get_center() if hasattr(n, "grad") else n.get_center()

    def pulse(self, name: str) -> VGroup:
        """The gradient in transit: a magenta dot with a soft halo on `name`'s grad."""
        core = Dot(radius=PULSE_RADIUS, color=S.STRUCTURE).set_stroke(S.FG, width=3)
        halo = Dot(radius=PULSE_RADIUS * 2, color=S.STRUCTURE, fill_opacity=S.OP_GHOST)
        return VGroup(halo, core).move_to(self.at(name))

    def travel(self, dot: VGroup, name: str) -> Animation:
        """Move the pulse backwards along the edge to `name` (straight, predictable)."""
        return dot.animate.move_to(self.at(name))
