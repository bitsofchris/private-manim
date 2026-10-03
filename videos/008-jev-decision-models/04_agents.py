"""Beat 4 (10.53 s): an agent loop is a ring of small fixed-choice decisions.

VO (23.25-33.78 s): "Now that matters because agents make a lot of decisions.
Which tool should I use? Is this action allowed? Am I done yet? Each one is a
choice from a fixed set of options, and that's what a classifier does."
Frame 0 is the loop circle with a teal dot already riding it. On "decisions"
three empty diamonds pop onto the ring; each question lights its diamond
magenta and hangs a chip on it; on "choice" every chip grows its option
squares; on "classifier" the probability bars fill in the middle of the loop
(they do not fit beside a diamond at the text floor). The dot stops on the
first diamond at the end. No scene captions (VO captions are burned in later).

Render:
    cd videos/008-jev-decision-models && uv run --no-sync manim -qh 04_agents.py Agents
    # -> media/videos/04_agents/1920p30/Agents.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot
from videos._shared.transformer import label
import _parts

BEAT_SECONDS = 10.53   # exact VO window of this beat
T_DECISIONS = 2.1      # VO: "decisions" (2.1-2.6)
T_TOOL = 3.3           # VO: "tool" in "Which tool should I use?"
T_ALLOWED = 4.6        # VO: "allowed"
T_DONE = 5.35          # VO: "done"
T_CHOICE = 6.8         # VO: "choice" in "a choice from a fixed set"
T_CLASSIFIER = 9.0     # VO: "classifier"; the bars fill over one HOLD
T_STOP = T_CLASSIFIER + S.HOLD   # the dot stops when the bars are full
LAP = 2 * S.HOLD       # one trip around the loop: 4.25 laps by T_STOP
START_ANGLE = 7 * PI / 6   # 8 o'clock; 4.25 laps on it rests at ~11 o'clock, just before 12

RADIUS = 1.75
DIAMOND = 0.6          # side of the rotated square
OPTION = 0.22          # side of one tiny option square
CHIP_GAP = 0.2
QUESTIONS = ["which tool?", "allowed?", "done?"]
OPTIONS = [3, 2, 2]    # search / code / ask, yes / no, yes / no
PROBS = [0.82, 0.11, 0.07]


def diamond() -> Square:
    return Square(side_length=DIAMOND, stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 2,
                  fill_opacity=0).rotate(PI / 4)


def option_squares(n: int) -> VGroup:
    return VGroup(*[
        Square(side_length=OPTION, stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 2)
        for _ in range(n)
    ]).arrange(RIGHT, buff=0.12)


class Agents(BocShortScene):
    def play(self, *args, **kwargs):
        # Manim 0.18.1 feeds updaters dt=0 on the first frame of every play, so a
        # dt-summing clock lags one frame per play. Resync to renderer time
        # (which is exact at play boundaries) after each play.
        super().play(*args, **kwargs)
        self.clock.set_value(self.renderer.time)

    def construct(self):
        centre = self.stage.get_center() + DOWN * 0.1
        ring = Circle(radius=RADIUS, stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 3)
        ring.move_to(centre)
        name = label("agent", S.FG_DIM).next_to(ring.get_top(), DOWN, buff=0.75)

        # The dot rides clockwise at a constant rate from frame 0. Scene time
        # drives it (see `play` below) so it stops just short of the top diamond.
        self.clock = ValueTracker(0.0)
        self.clock.add_updater(lambda m, dt: m.increment_value(dt))

        def ride(m):
            a = START_ANGLE - TAU * self.clock.get_value() / LAP
            m.move_to(centre + RADIUS * np.array([np.cos(a), np.sin(a), 0]))
        dot = data_dot(radius=S.DOT_SHORT)
        dot.add_updater(ride, call_updater=True)
        self.add(ring, name, self.clock, dot)

        # "decisions": three empty diamonds at 12, 4 and 8 o'clock.
        angles = [PI / 2, -PI / 6, 7 * PI / 6]
        diamonds = VGroup(*[
            diamond().move_to(centre + RADIUS * np.array([np.cos(a), np.sin(a), 0])) for a in angles
        ])
        self.hold_until(T_DECISIONS)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in diamonds], lag_ratio=0.3),
                  run_time=S.BEAT)
        self.remove(dot)
        self.add(dot)   # the dot passes over the diamonds

        # Chips hang outward: above the top diamond, below the two lower ones,
        # pushed to the safe edges so the lower pair never touch.
        chips = VGroup(*[_parts.chip_text(q) for q in QUESTIONS])
        chips[0].next_to(diamonds[0], UP, buff=CHIP_GAP)
        chips[1].next_to(diamonds[1], DOWN, buff=0.6).align_to(self.safe, RIGHT)
        chips[2].next_to(diamonds[2], DOWN, buff=0.6).align_to(self.safe, LEFT)
        for t, chip, d in zip([T_TOOL, T_ALLOWED, T_DONE], chips, diamonds):
            self.hold_until(t)
            self.play(FadeIn(chip),
                      d.animate.set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE)
                               .set_fill(S.STRUCTURE, opacity=S.OP_GHOST),
                      run_time=S.BEAT)

        # "choice ... fixed set of options": tiny option squares, outward of each chip.
        options = VGroup(*[option_squares(n) for n in OPTIONS])
        options[0].next_to(chips[0], UP, buff=0.15)
        options[1].next_to(chips[1], DOWN, buff=0.15)
        options[2].next_to(chips[2], DOWN, buff=0.15)
        self.hold_until(T_CHOICE)
        self.play(Create(options, lag_ratio=0.1), run_time=S.BEAT)

        # "classifier": the bars from beat 2 fill inside the loop (bars only; the
        # names would be below the text floor beside a diamond).
        bars = _parts.ProbBars(["search", "code", "ask"], width=5.6)
        bars.bars.scale_to_fit_height(1.4).next_to(name, DOWN, buff=0.25)
        bars.bars.align_to([centre[0] - 0.6, 0, 0], LEFT)   # longest bar stays inside the ring
        self.add(bars.bars)
        fill = [a for a in bars.fill_to(PROBS).animations if a.mobject in bars.bars]
        self.hold_until(T_CLASSIFIER)
        self.play(AnimationGroup(*fill), run_time=S.HOLD)

        dot.clear_updaters()   # T_STOP: the dot rests just before the top diamond
        self.clock.clear_updaters()
        self.hold_until(BEAT_SECONDS)
