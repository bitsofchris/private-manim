"""Beat 2 (7.34 s): a neuron has a weight per input plus a bias, all random at first.

VO (scene-local s): "Each neuron has its own weight per input" 0.0-2.3,
"and a special term called a bias" 2.3-4.2, "The parameters of your network
are initialized randomly" 4.2-7.3. Word times from silencedetect on
vo_final.wav. No scene captions: VO captions are burned in later (self.band).

Render:
    cd videos/004-backprop-short && uv run --no-sync manim -qh 02_neuron.py Neuron
    # -> media/videos/02_neuron/1920p30/Neuron.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot

BEAT_SECONDS = 7.42   # exact VO window of this beat
T_WEIGHT = 1.35       # VO: "weight per input"
T_BIAS = 2.75         # slide starts on "called a", lands on "bias"
T_RANDOM = 5.25       # VO: "initialized randomly"

# Layout (searched so no label touches a line, dot, the neuron or the stage
# edge). The lines converge, so the wedge between x1 and x2 is only tall
# enough for the stacked w2 label right next to the x2 dot: w2 sits there,
# w1 above the top line and w3 below the bottom one.
INPUT_SPREAD = 0.455  # input y offsets as a fraction of stage height
X_LABEL_BUFF = 0.2
NEURON_R = 1.0
NEURON_X_FRAC = 0.78  # neuron centre, fraction of stage width from the left
ARROW_LEN = 0.9       # tip may reach the right UI rail; the "y" label stays safe
SHORT_STROKE = S.STROKE_STRUCTURE * 1.6  # 5 px reads hairline on a phone
LABEL_T = [0.7, None, 0.7]  # outer labels: where along the line; w2 hugs its dot
LABEL_SIDE = [1, 1, -1]     # +1 = label above its line, -1 = below
LABEL_GAP = 0.12
BIAS_RISE = 2.0       # "+ b" slides up this far into the neuron


def label(s: str, color: str) -> Text:
    return Text(s, font=S.FONT, weight="MEDIUM").scale(S.SHORT_LABEL_SCALE).set_color(color)


def weight_label(i: int, value: float) -> VGroup:
    """'w1' stacked over its value: a one-line 'w1 = +0.53' is wider than the line."""
    return VGroup(label(f"w{i + 1}", S.STRUCTURE), label(f"{value:+.2f}", S.STRUCTURE)
                  ).arrange(DOWN, buff=0.1)


def place_clear(lbl: Mobject, line: Line, t: float, side: int) -> None:
    """Horizontal text over a sloped line: clearance covers the line's rise
    across half the label's width, plus half the label's height (from 003)."""
    d = normalize(line.get_end() - line.get_start())
    slope = abs(d[1] / d[0])
    clearance = LABEL_GAP + lbl.height / 2 + lbl.width / 2 * slope
    lbl.move_to(line.point_from_proportion(t) + UP * side * clearance)


class Neuron(BocShortScene):
    def construct(self):
        rng = np.random.default_rng(S.SEED)
        finals = rng.uniform(-1, 1, size=6).round(2)[3:]  # second triple has mixed signs
        st = self.stage
        cy, h = st.get_y(), st.height
        center = np.array([st.get_left()[0] + st.width * NEURON_X_FRAC, cy, 0.0])

        neuron = Circle(radius=NEURON_R, color=S.FG, stroke_width=SHORT_STROKE)
        neuron.set_fill(S.BG_PANEL, opacity=1).move_to(center)
        out_arrow = Arrow(neuron.get_right(), neuron.get_right() + RIGHT * ARROW_LEN, buff=0.1,
                          color=S.FG_DIM, stroke_width=SHORT_STROKE,
                          max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)
        y_lbl = label("y", S.FG).next_to(out_arrow, UP, buff=0.15)

        dots, xs, lines, labels = VGroup(), VGroup(), VGroup(), VGroup()
        # One column for all dots, clear of the widest x label.
        pad = max(label(f"x{i}", S.DATA).width for i in (1, 2, 3)) + X_LABEL_BUFF + S.DOT_SHORT
        for i, off in enumerate([INPUT_SPREAD, 0.0, -INPUT_SPREAD]):
            x_lbl = label(f"x{i + 1}", S.DATA)
            p = np.array([st.get_left()[0] + pad, cy + off * h, 0.0])
            dots.add(data_dot(p, radius=S.DOT_SHORT).set_opacity(1))
            xs.add(x_lbl.next_to(dots[-1], LEFT, buff=X_LABEL_BUFF))
            end = center + NEURON_R * normalize(p - center)
            lines.add(Line(p, end, color=S.STRUCTURE, stroke_width=SHORT_STROKE))
            lbl = weight_label(i, rng.uniform(-1, 1))
            t = LABEL_T[i]
            if t is None:  # left edge one gap past the dot
                t = (S.DOT_SHORT + LABEL_GAP + lbl.width / 2) / lines[-1].get_length()
            place_clear(lbl, lines[-1], t, LABEL_SIDE[i])
            labels.add(lbl)

        # Frame 0: inputs and output on screen; "Each neuron" grows in at once.
        self.add(dots, xs, out_arrow, y_lbl)
        self.play(GrowFromCenter(neuron), run_time=S.BEAT)

        # "weight per input": the magenta weights wire each input to the neuron.
        # Lines go in under the neuron so they tuck behind its filled disc
        # (add order, not z_index: see STYLE.md gotchas).
        self.hold_until(T_WEIGHT)
        self.add(lines)
        self.bring_to_front(neuron)
        self.play(Create(lines, lag_ratio=0.2), FadeIn(labels, lag_ratio=0.2), run_time=S.HOLD)

        # "a bias": gold "+ b" rises into the neuron.
        self.hold_until(T_BIAS)
        bias = label("+ b", S.CONTENT_GOLD).move_to(neuron)
        self.play(FadeIn(bias, shift=UP * BIAS_RISE), run_time=S.HOLD)

        # "initialized randomly": each weight's value spins, then settles.
        self.hold_until(T_RANDOM)
        spin = ValueTracker(0)
        for lbl, final in zip(labels, finals):
            def spinner(num, final=final):
                t = spin.get_value()
                v = final if t >= 1 else final + (1 - t) * rng.uniform(-1, 1)
                num.become(label(f"{v:+.2f}", S.STRUCTURE).move_to(num))
            lbl[1].add_updater(spinner)
        self.play(spin.animate.set_value(1), run_time=S.HOLD, rate_func=linear)
        for lbl in labels:
            lbl[1].clear_updaters()
        self.hold_until(BEAT_SECONDS)  # still resting frame
