"""Code card in the caption band, shared by beats 2-6 of 007.

The card sits at the top of the band; the burned-in VO captions sit at the
bottom (`assemble.py --captions-anchor bottom`), so a beat has both.

    card = code_card(self.band, [7, 8])          # lines of transformer.GPT_SOURCE
    self.play(FadeIn(card), run_time=S.BEAT)
    self.play(highlight_lines(card, 1), run_time=S.BEAT)   # 1-based within the card
"""
from __future__ import annotations

from manim import DOWN, UP, Code, Mobject

from videos._shared import style as S
from videos._shared.mobjects import code_block
from videos._shared.transformer import GPT_SOURCE

LINES = GPT_SOURCE.splitlines()
CARD_W_FRAC = 0.96   # of the band width
CARD_TOP_MARGIN = 0.1   # below the band top (the stage edge)


def card_source(line_numbers: list[int]) -> str:
    """The chosen 1-based lines of GPT_SOURCE, re-dedented so the card is flush."""
    picked = [LINES[n - 1] for n in line_numbers]
    indent = min(len(l) - len(l.lstrip()) for l in picked if l.strip())
    return "\n".join(l[indent:] for l in picked)


def code_card(band: Mobject, line_numbers: list[int], highlight=None) -> Code:
    """A code_block of those lines, centred in the band, never wider than it."""
    card = code_block(card_source(line_numbers), highlight=highlight)
    if card.width > band.width * CARD_W_FRAC:
        card.scale_to_fit_width(band.width * CARD_W_FRAC)
    # Top of the band: the burned-in VO captions sit at the bottom
    # (assemble.py --captions-anchor bottom), so both fit.
    return card.move_to(band).align_to(band, UP).shift(DOWN * CARD_TOP_MARGIN)
