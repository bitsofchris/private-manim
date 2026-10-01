"""Beat 1 (3.99 s): the block diagram draws itself in, bottom to top. Nothing is magenta yet.

VO (0.00-3.99 s): "Here's how you can understand AI architecture diagrams like a pro."
Frame 0 has the whole diagram on screen as a faint ghost; the real FG_DIM marks
and teal arrows trace over it from the bottom, finishing on "diagrams". Still
through "like a pro". Last frame: the untouched build_block output, which is
the opening state of every later beat.

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -qh --disable_caching 01_hook.py Hook
    # -> media/videos/01_hook/1920p30/Hook.mp4 (cached partials can drop a frame; keep --disable_caching)
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import build_block, ROWS

BEAT_SECONDS = 3.99   # exact VO window of this beat
T_DRAW_TOP = S.HOLD   # VO: "architecture" -> the upper half starts; both halves end on "diagrams" (~2.4 s)
DRAW_LAG = 0.35       # stagger inside each half so the column visibly climbs


def draw_order(d) -> list[Mobject]:
    """The diagram's parts in the order a reader meets them: bottom to top,
    each arrow right after the row it leaves, skips when their branch exists."""
    out: list[Mobject] = []
    for i, r in enumerate(ROWS):
        out.append(d.rows[r])
        if i < len(d.flow):
            out.append(d.flow[i])
        if r == "attn":
            out.append(d.skips[0])
        if r == "ffn":
            out.append(d.skips[1])
    out.append(d.bracket)
    return out


def ghost_of(m: Mobject, k: float) -> Mobject:
    """A faint copy: every stroke and fill opacity scaled by k (no set_opacity:
    in 0.18.1 it fills stroke-only paths)."""
    g = m.copy()
    for sub in g.family_members_with_points():
        sub.set_stroke(opacity=sub.get_stroke_opacity() * k)
        sub.set_fill(opacity=sub.get_fill_opacity() * k)
    return g


class Hook(BocShortScene):
    def construct(self):
        d = build_block(self.stage)
        ghost = ghost_of(d, S.OP_GHOST)
        parts = draw_order(d)
        half = len(parts) // 2
        lower, upper = VGroup(*parts[:half]), VGroup(*parts[half:])
        # Frame 0: only the faint whole diagram is there; the real marks draw
        # over it from the bottom (d itself is added once it is complete, so
        # the upper half is not visible before its turn). Layer by add() order.
        self.add(ghost)

        # "Here's how you can understand": Embed -> Attention -> (+) climbs in.
        self.play(Create(lower, lag_ratio=DRAW_LAG), run_time=S.HOLD)
        # "AI architecture diagrams": FFN -> (+) -> Linear and the N× bracket.
        self.hold_until(T_DRAW_TOP)
        self.play(Create(upper, lag_ratio=DRAW_LAG), run_time=S.HOLD)
        # The wrapper groups and the ghost are scaffolding: leave only d on screen.
        self.remove(lower, upper, ghost)
        self.add(d)

        # "like a pro": hold still on the complete dim diagram.
        self.hold_until(BEAT_SECONDS)
