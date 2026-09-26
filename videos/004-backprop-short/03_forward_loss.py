"""Beat 3 (9.07 s): the forward pass turns a sample into an output; its gap to the target is the loss.

VO (scene-local): "The forward pass is when you take" 0.0-1.6 / "the current
training sample," 1.6-3.1 / "feed it to the model," 3.1-4.0 / "and get the
model's output." 4.3-5.7 / "This comparison allows us to compute the loss."
5.7-9.07 ("loss" ~8.4). Captions are burned in later; none here.

Render:
    cd videos/004-backprop-short && uv run --no-sync manim -qh 03_forward_loss.py ForwardLoss
    # -> media/videos/03_forward_loss/1920p30/ForwardLoss.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot

DURATION = 9.07
T_SAMPLE = 0.1                   # x enters frame ~0.3 s, lands 1.3 s ("forward pass")
T_PASSES = (3.1, 3.7, 4.5)       # pulse per layer: "feed it to the model" .. "model's"
T_OUTPUT, T_COMPARE, T_LOSS = 5.1, 6.0, 8.4  # "output" / "comparison" / "loss"
OUTPUT, TARGET = 0.2, 1.0
LOSS = (TARGET - OUTPUT) ** 2
NODE_R = 0.55
SCALE_X = 0.5                    # x of the vertical value scale
SCALE_Y0, SCALE_UNIT = -0.95, 5.6  # y of value 0.0; scene units per 1.0
ROW_Y = [4.7, 2.45, SCALE_Y0 + OUTPUT * SCALE_UNIT]  # input / hidden / output (top to bottom)
ROW_X = [[-2.75, -1.25], [-3.5, -2.0, -0.5], [-2.0]]
SAMPLE_Y = 5.75                  # sample dot sits above the input row
EDGE_WIDTH = S.STROKE_AXIS * 2
BAR_WIDTH = S.STROKE_STRUCTURE * 5   # the magenta loss bar reads thick on a phone
IDLE_AMP = 0.25                  # faint breathing of node rings before the sample
LIT = dict(fill_color=S.DATA, fill_opacity=S.OP_DATA, stroke_color=S.DATA)


def label(top: str, bottom: str, color: str) -> VGroup:
    """Two-line label: word over value, left-aligned, phone-legible."""
    lines = [Text(s, font=S.FONT, weight="MEDIUM").scale(S.SHORT_LABEL_SCALE) for s in (top, bottom)]
    return VGroup(*lines).arrange(DOWN, buff=0.12, aligned_edge=LEFT).set_color(color)


def value_pt(v: float) -> np.ndarray:
    return np.array([SCALE_X, SCALE_Y0 + v * SCALE_UNIT, 0])


def after(frac: float):
    """Rate func that waits until `frac` of the run, then eases in (node lights as pulse arrives)."""
    return lambda t: smooth(min(max((t - frac) / (1 - frac), 0), 1))


def link(a: Mobject, b: Mobject) -> Line:
    d = normalize(b.get_center() - a.get_center())
    return Line(a.get_center() + d * a.width / 2, b.get_center() - d * b.width / 2,
                stroke_color=S.MUTED, stroke_width=EDGE_WIDTH)


class ForwardLoss(BocShortScene):
    def construct(self):
        layers = [VGroup(*[Circle(radius=NODE_R, stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 2.5,
                                  fill_color=S.DATA, fill_opacity=0)
                           .move_to([x, y, 0]) for x in xs]) for xs, y in zip(ROW_X, ROW_Y)]
        edges = [VGroup(*[link(a, b) for a in la for b in lb]) for la, lb in zip(layers, layers[1:])]
        nodes = VGroup(*layers)
        self.add(*edges, nodes)

        # Network idles with a faint pulse until the sample is fed in.
        idle = lambda m: m.set_stroke(opacity=1 - IDLE_AMP * (1 + np.sin(4 * self.renderer.time)) / 2)
        nodes.add_updater(idle)
        self.hold_until(T_SAMPLE)

        # "The forward pass": teal x slides down into place above the inputs.
        x_dot = data_dot([np.mean(ROW_X[0]), SAMPLE_Y, 0], radius=S.DOT_SHORT).set_opacity(1)
        x_lbl = Text("x", font=S.FONT, weight="MEDIUM").scale(S.SHORT_LABEL_SCALE).set_color(S.DATA)
        x_lbl.next_to(x_dot, RIGHT, buff=0.3)
        sample = VGroup(x_dot, x_lbl)
        feed = VGroup(*[link(x_dot, n) for n in layers[0]])
        target_pos = sample.get_center()
        sample.shift(UP * 3)
        self.play(sample.animate.move_to(target_pos), FadeIn(feed), run_time=S.HOLD)

        # "feed it to the model ... output": pulse travels down, layer by layer.
        self.hold_until(T_PASSES[0])
        nodes.remove_updater(idle).set_stroke(opacity=1)
        for t, es, layer in zip(T_PASSES, [feed, *edges], layers):
            self.hold_until(t)
            flash = es.copy().set_stroke(S.HIGHLIGHT, width=S.STROKE_STRUCTURE)
            self.play(ShowPassingFlash(flash, time_width=0.6),
                      layer.animate(rate_func=after(0.5)).set_style(**LIT), run_time=S.BEAT)

        # "output": the value slides out beside the output node.
        self.hold_until(T_OUTPUT)
        out_node = layers[-1][0]
        out_dot = data_dot(value_pt(OUTPUT), radius=S.DOT_SHORT).set_opacity(1)
        out_lbl = label("output", f"{OUTPUT:.1f}", S.DATA).next_to(out_dot, RIGHT, buff=0.35)
        self.play(TransformFromCopy(out_node, out_dot), FadeIn(out_lbl, shift=RIGHT * 0.2), run_time=S.BEAT)

        # "comparison": a small vertical scale with the target on it.
        self.hold_until(T_COMPARE)
        scale = Line(value_pt(0), value_pt(TARGET + 0.08), stroke_color=S.FG_DIM, stroke_width=EDGE_WIDTH)
        ticks = VGroup(*[Line(LEFT * 0.2, RIGHT * 0.2, stroke_color=S.FG_DIM, stroke_width=EDGE_WIDTH)
                         .move_to(value_pt(0))])
        tgt_tick = Line(LEFT * 0.35, RIGHT * 0.35, stroke_color=S.FG, stroke_width=S.STROKE_STRUCTURE)
        tgt_tick.move_to(value_pt(TARGET))
        tgt_lbl = label("target", f"{TARGET:.1f}", S.FG).next_to(tgt_tick, RIGHT, buff=0.35).align_to(out_lbl, LEFT)
        self.add_foreground_mobject(out_dot)
        self.play(Create(scale), FadeIn(ticks), Create(tgt_tick), FadeIn(tgt_lbl, shift=RIGHT * 0.2),
                  run_time=S.HOLD)

        # "the loss": the gap fills with the thick magenta bar (the hero).
        self.hold_until(T_LOSS)
        bar = Line(value_pt(OUTPUT), value_pt(TARGET), stroke_color=S.STRUCTURE, stroke_width=BAR_WIDTH)
        loss_lbl = label("loss", f"{LOSS:.2f}", S.STRUCTURE).next_to(bar, RIGHT, buff=0.35)
        loss_lbl.align_to(out_lbl, LEFT)
        self.add_foreground_mobjects(tgt_tick)
        self.play(Create(bar), FadeIn(loss_lbl, shift=RIGHT * 0.2), run_time=S.BEAT)
        self.hold_until(DURATION)
