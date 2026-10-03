"""Reusable parts for the Jev Short (008): probability bars, cards, chips.

The probability bars are the thing that keeps its identity across beats 2,
4 and 6 (ANIMATION_RULES rule 8), so every beat builds them here and
animates them with `fill_to`, never a fade-swap.

    bars = ProbBars(["yes", "no", "later"], width=5.0)      # all bars at 0
    self.add(bars)
    self.play(bars.fill_to([0.91, 0.06, 0.03]), run_time=S.HOLD)

    card = text_card(["{ from: 'ceo@...',", "  subject: 'server down' }"])
    chip = chip_text("yes")
"""
from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    AnimationGroup,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos._shared import style as S
from videos._shared.transformer import label

BAR_H = 0.5              # bar height; label height is ~0.64 so rows pitch at ~0.95
ROW_BUFF = 0.3
LABEL_W = 2.4            # column for the choice names
VALUE_W = 1.5            # column for the "0.91" text
VALUE_GAP = 0.2          # between the longest possible bar and the value
MONO_SCALE = S.SHORT_LABEL_SCALE * 0.6   # Menlo is wide; this is ~the code-card size
MAX_CARD_W = 7.0         # a card never exceeds the stage width
CARD_PAD = 0.25
CHIP_PAD = 0.15
MIN_BAR = 0.02           # a zero-probability bar is still a sliver, so it can grow


def bar_width(prob: float, max_width: float) -> float:
    """Bar length for a probability. Pure; unit-tested."""
    if not 0.0 <= prob <= 1.0:
        raise ValueError(f"probability {prob} outside [0, 1]")
    return max(MIN_BAR, prob * max_width)


def mono(text: str, color: str = S.FG) -> Text:
    """Monospace text at the phone floor, for JSON-ish cards and values."""
    return Text(text, font=S.FONT_MONO).scale(MONO_SCALE).set_color(color)


class ProbBars(VGroup):
    """One row per choice: name, teal bar, value. `.bars`, `.names`, `.values`.

    Bars start at zero. `fill_to(probs)` returns an AnimationGroup that grows
    each bar from its left edge and updates the value text in place.
    """

    def __init__(self, choices: list[str], width: float, color: str = S.DATA):
        super().__init__()
        self.choices = choices
        self.max_width = width - LABEL_W - VALUE_GAP - VALUE_W
        self.names = VGroup(*[label(c, S.FG) for c in choices])
        self.bars = VGroup(*[
            Rectangle(width=MIN_BAR, height=BAR_H, fill_color=color, fill_opacity=S.OP_DATA,
                      stroke_width=0)
            for _ in choices
        ])
        self.values = VGroup(*[mono("0.00", S.FG_DIM) for _ in choices])
        rows = VGroup()
        for name, bar, value in zip(self.names, self.bars, self.values):
            # One invisible full-width slot per row so rows align and arrange cleanly.
            slot = Rectangle(width=width, height=max(BAR_H, name.height),
                             stroke_opacity=0, fill_opacity=0)
            x0 = slot.get_left()[0]
            name.move_to(slot).align_to(slot, LEFT)
            bar.move_to(slot).align_to([x0 + LABEL_W, 0, 0], LEFT)
            value.move_to(slot).align_to([x0 + LABEL_W + self.max_width + VALUE_GAP, 0, 0], LEFT)
            rows.add(VGroup(slot, name, bar, value))
        rows.arrange(DOWN, buff=ROW_BUFF)
        self.add(rows)
        self.rows = rows

    def fill_to(self, probs: list[float]) -> AnimationGroup:
        anims = []
        for bar, value, p in zip(self.bars, self.values, probs):
            w = bar_width(p, self.max_width)
            target = bar.copy().stretch_to_fit_width(w).align_to(bar, LEFT)
            new_value = mono(f"{p:.2f}", S.FG if p == max(probs) else S.FG_DIM)
            new_value.move_to(value).align_to(value, LEFT)
            anims.append(bar.animate.become(target))
            anims.append(value.animate.become(new_value))
        return AnimationGroup(*anims)


def text_card(lines: list[str], color: str = S.FG_DIM, max_width: float = MAX_CARD_W) -> VGroup:
    """A BG_PANEL card with monospace lines (an input state, a question).
    Wider than `max_width` -> scaled down to fit (keep lines short instead)."""
    body = VGroup(*[mono(l, color) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    if body.width > max_width - 2 * CARD_PAD:
        body.scale_to_fit_width(max_width - 2 * CARD_PAD)
    box = RoundedRectangle(corner_radius=0.2, width=body.width + 2 * CARD_PAD,
                           height=body.height + 2 * CARD_PAD, fill_color=S.BG_PANEL,
                           fill_opacity=1, stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 2)
    g = VGroup(box, body.move_to(box))
    g.box, g.body = box, body
    return g


def chip_text(text: str, color: str = S.FG) -> VGroup:
    """A small rounded chip: one answer option."""
    t = label(text, color)
    box = RoundedRectangle(corner_radius=0.3, width=t.width + 2 * CHIP_PAD,
                           height=t.height + 2 * CHIP_PAD, fill_color=S.BG_PANEL, fill_opacity=1,
                           stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 2)
    g = VGroup(box, t.move_to(box))
    g.box, g.text = box, t
    return g
