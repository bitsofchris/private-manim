"""Beat 1 (6.20 s): a transformer takes tokens in and a matrix of updated tokens comes out the top.

VO (scene-local s): "A transformer takes a sequence of tokens" 0.3-2.8
("tokens" ~2.3); "and produces updated representations of those tokens"
2.8-6.2 ("updated representations" ~3.9-5.2). No scene captions: VO captions
are burned in later over self.band.

Bird's-eye opener on the shared block diagram. Frame 0: the dim diagram fills
the stage with the sentence "my name is" under Embed. The words are drawn
into Embed, a HIGHLIGHT pulse climbs the N× block and stops above the second
(+); there a tiny token matrix pops in with the same three words shrunk above
its columns. Nothing is magenta.
Ends: dim diagram + tiny matrix + tiny words above the N× block. Beat 2
imports `opening_state` to open on this exact frame.

Layout: the diagram is built on a rect just tall enough for its rows (gaps at
the shared MIN_GAP) and scaled by DIAGRAM_SCALE so the sentence fits under it
and a slot opens above the N× block once Linear is lifted back to the stage
top. The box labels end up 0.8 x SHORT_LABEL_SCALE (see the report).

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh 01_hook.py Hook
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
from _tokens import TOKENS, VALUES, WORD_BUFF, label

BEAT_SECONDS = 6.20
T_PULSE = 1.2         # pulse leaves Embed as the words finish going in; stops at the N× top on "tokens" (~2.3)
T_UPDATED = 3.9       # VO: "updated representations": the tiny matrix pops out
SENTENCE_BUFF = 0.35  # word spacing when the three words still read as one sentence
WORDS_BUFF = 0.25     # sentence to Embed box
DIAGRAM_SCALE = 0.8   # see module docstring
ROWS_HEIGHT = 6.45    # rect height the rows are stacked in (gap just over transformer.MIN_GAP)
TINY_WIDTH_FRAC = 0.7  # tiny matrix width as a fraction of a box width
ABSORB_SCALE = 0.4    # the words shrink by this as Embed takes them in
PULSE_WIDTH = 0.6     # ShowPassingFlash time_width on the flow arrows


def opening_state(stage: Mobject) -> tuple[T.BlockDiagram, TokenMatrix, VGroup]:
    """The frame beat 1 ends on and beat 2 opens on: (diagram, tiny_matrix, tiny_words)."""
    words_h = label(TOKENS[1]).height
    rows_rect = _rect(SafeBounds(stage.get_left()[0], stage.get_right()[0],
                                 stage.get_top()[1] - ROWS_HEIGHT, stage.get_top()[1]))
    d = T.build_block(rows_rect)
    d.scale(DIAGRAM_SCALE)
    d.align_to(stage, DOWN).shift(UP * (words_h + 2 * WORDS_BUFF))
    # Lift Linear to the stage top: the slot above the N× block is for the matrix.
    head = d.rows["head"]
    head.align_to(stage, UP)
    d.flow[-1].put_start_and_end_on(d.rows["add2"].get_top(), head.get_bottom())

    tiny = TokenMatrix(VALUES[0], digits=False, bracketed=False)
    k = head.width * TINY_WIDTH_FRAC / tiny.width
    tiny.scale(k)
    tiny_words = VGroup(*[label(w).scale(k).next_to(c, UP, buff=WORD_BUFF * k)
                          for w, c in zip(TOKENS, tiny.columns)])
    slot_y = (d.rows["add2"].get_top()[1] + head.get_bottom()[1]) / 2
    VGroup(tiny, tiny_words).move_to([head.get_x(), slot_y, 0])
    return d, tiny, tiny_words


class HookV2(BocShortScene):
    def construct(self):
        d, tiny, tiny_words = opening_state(self.stage)
        embed = d.rows["embed"]

        # Frame 0: the dim diagram with the sentence under Embed.
        words = VGroup(*[label(w) for w in TOKENS]).arrange(RIGHT, buff=SENTENCE_BUFF)
        words.next_to(embed, DOWN, buff=WORDS_BUFF)
        self.add(d, words)

        # "takes a sequence of tokens": Embed takes the words in. Animated in
        # place (not FadeOut: its clean-up restores the mobject, and the words
        # must stay absorbed until they re-emerge as the tiny labels).
        self.play(*[w.animate.move_to(embed).scale(ABSORB_SCALE).set_opacity(0)
                    for w in words], run_time=S.HOLD)

        # ... and a pulse climbs the N× block: Attention, (+), FFN, (+).
        self.hold_until(T_PULSE)
        climb = d.flow[:-1]  # every arrow up to the top of the N× block
        trail = VGroup(*[a.copy().set_color(S.HIGHLIGHT) for a in climb])
        pulse = data_dot(climb[0].get_start(), radius=S.DOT_SHORT, color=S.HIGHLIGHT)
        pulse.set_opacity(1)
        path = Line(climb[0].get_start(), climb[-1].get_end())
        self.play(MoveAlongPath(pulse, path),
                  ShowPassingFlash(trail, time_width=PULSE_WIDTH), run_time=S.HOLD)

        # "updated representations": a tiny matrix pops out above the block, the
        # same words (now tiny) above its columns.
        self.hold_until(T_UPDATED)
        self.play(FadeOut(pulse), GrowFromCenter(tiny),
                  *[Transform(w, tw) for w, tw in zip(words, tiny_words)], run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)  # "of those tokens": still
