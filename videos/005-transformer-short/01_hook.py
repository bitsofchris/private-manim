"""Beat 1 (6.20 s): a transformer takes a matrix of tokens in and a matrix of updated tokens comes out.

VO (scene-local s): "A transformer takes a sequence of tokens" 0.3-2.8
("tokens" ~2.3); "and produces updated representations of those tokens"
2.8-6.2 ("updated representations" ~3.9-5.2). No scene captions: VO captions
are burned in later over self.band.

Bird's-eye opener on the shared block diagram at scale 1.0 (box labels at
SHORT_LABEL_SCALE). Frame 0: the dim diagram fills the stage with a small
bracketed "X" matrix beside Embed. X is absorbed into Embed, a HIGHLIGHT
pulse climbs the N× block and stops at its top (the second (+)); there a
same-size "X′" matrix pops out, between the block and Linear. Nothing is
magenta. Ends: dim diagram + X′ matrix + its label above the N× block. Beat 2
imports `opening_state` to open on this exact frame.

Layout: the six rows cannot share the stage with two in-column matrices at
readable size (rows alone are ~4.2 of the 7.25 units), so the input X sits
beside Embed in the free area left of the column (the N× bracket only spans
the block) and the whole diagram is shifted right to the stage edge to make
room for it. Only the output slot above the N× block is cut out of the row
stack: the rows are built on a rect shortened by the slot, Linear is lifted
back to the stage top and the last arrow re-drawn (so every other row gap is
equal). Embed bleeds below the stage by build_block's default (BOTTOM_BLEED)
and X sits level with it.

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh --disable_caching 01_hook.py Hook
    # -> media/videos/01_hook/1920p30/Hook.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene, _rect, SafeBounds
from videos._shared.mobjects import TokenMatrix, data_dot
from videos._shared import transformer as T
from _tokens import VALUES, label

BEAT_SECONDS = 6.20
T_PULSE = 1.2          # pulse leaves Embed as X finishes going in; at the N× top on "tokens" (~2.3)
T_UPDATED = 3.9        # VO: "updated representations": X′ pops out
MATRIX_WIDTH_FRAC = 0.46  # X / X′ width as a fraction of a box width (what fits beside Embed)
SLOT_BELOW = 0.12      # (+) top -> X′ bottom
SLOT_ABOVE = 0.30      # X′ top -> Linear bottom: the arrow tip (0.28) stays visible
X_BUFF = 0.15          # X matrix -> Embed box
LABEL_BUFF = 0.10      # "X" / "X′" -> their matrix
RIGHT_MARGIN = 0.05    # diagram's right edge -> stage right
ABSORB_SCALE = 0.4     # X shrinks by this as Embed takes it in
PULSE_WIDTH = 0.6      # ShowPassingFlash time_width on the flow arrows


def small_matrix(values, box_width: float) -> TokenMatrix:
    """A digit-less bracketed matrix scaled to MATRIX_WIDTH_FRAC of a box."""
    m = TokenMatrix(values, digits=False, bracketed=True)
    return m.scale(box_width * MATRIX_WIDTH_FRAC / m.width)


def opening_state(stage: Mobject) -> tuple[T.BlockDiagram, TokenMatrix, Text]:
    """The frame beat 1 ends on and beat 2 opens on: (diagram, X′ matrix, "X′")."""
    probe = T.build_block(stage)  # row heights and the box width, nothing else
    heights = [probe.rows[r].height for r in T.ROWS]
    box_w = probe.rows["embed"].width
    out = small_matrix(VALUES[1], box_w)
    # Cut the X′ slot out of the row stack; the remaining gaps stay equal.
    span = stage.height + T.BOTTOM_BLEED
    slot = out.height + SLOT_BELOW + SLOT_ABOVE
    gap = (span - sum(heights) - slot) / (len(T.ROWS) - 2)
    rows_rect = _rect(SafeBounds(stage.get_left()[0], stage.get_right()[0],
                                 stage.get_bottom()[1], stage.get_top()[1] - (slot - gap)))
    d = T.build_block(rows_rect)
    head = d.rows["head"]
    head.align_to(stage, UP)
    d.flow[-1].put_start_and_end_on(d.rows["add2"].get_top(), head.get_bottom())
    d.shift(RIGHT * (stage.get_right()[0] - RIGHT_MARGIN - d.get_right()[0]))

    out.next_to(d.rows["add2"], UP, buff=SLOT_BELOW).set_x(head.get_x())
    out_label = label("X′", S.DATA).next_to(out, RIGHT, buff=LABEL_BUFF)
    return d, out, out_label


class Hook(BocShortScene):
    def construct(self):
        d, out, out_label = opening_state(self.stage)
        embed = d.rows["embed"]

        # Frame 0: the dim diagram with the input matrix X beside Embed.
        inp = small_matrix(VALUES[0], embed.width).next_to(embed, LEFT, buff=X_BUFF)
        inp.set_y(embed.get_y())
        inp_label = label("X", S.DATA).next_to(inp, LEFT, buff=LABEL_BUFF)
        if inp_label.get_left()[0] < self.stage.get_left()[0]:
            raise ValueError("X label leaves the stage: shrink MATRIX_WIDTH_FRAC")
        self.add(d, inp, inp_label)

        # "takes a sequence of tokens": Embed takes X in. Animated in place (a
        # FadeOut's clean-up would restore the mobject).
        self.play(*[m.animate.move_to(embed).scale(ABSORB_SCALE).set_opacity(0)
                    for m in (inp, inp_label)], run_time=S.HOLD)

        # ... and a pulse climbs the N× block: Attention, (+), FFN, (+).
        self.hold_until(T_PULSE)
        climb = d.flow[:-1]  # every arrow up to the top of the N× block
        trail = VGroup(*[a.copy().set_color(S.HIGHLIGHT) for a in climb])
        pulse = data_dot(climb[0].get_start(), radius=S.DOT_SHORT, color=S.HIGHLIGHT)
        pulse.set_opacity(1)
        path = Line(climb[0].get_start(), climb[-1].get_end())
        self.play(MoveAlongPath(pulse, path),
                  ShowPassingFlash(trail, time_width=PULSE_WIDTH), run_time=S.HOLD)

        # "updated representations": X′ pops out above the block, under Linear.
        self.hold_until(T_UPDATED)
        self.play(FadeOut(pulse), GrowFromCenter(out), FadeIn(out_label), run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)  # "of those tokens": still
