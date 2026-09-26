"""Preconfigured mobjects in the Bits of Chris palette.

Always prefer these over raw Dot/Arrow/Axes so the palette stays consistent.
"""
from __future__ import annotations

from collections.abc import Iterable

from manim import (
    Arrow,
    Arrow3D,
    Axes,
    Code,
    DashedLine,
    Dot,
    Dot3D,
    NumberPlane,
    Rectangle,
    ThreeDAxes,
    Transform,
)
from pygments.style import Style
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Token,
)

from videos._shared import style as S


def data_dot(point=None, **kwargs) -> Dot:
    """A 2D data point in the TEAL hero color."""
    d = Dot(
        color=kwargs.pop("color", S.DATA),
        radius=kwargs.pop("radius", S.DOT_DATA),
        **kwargs,
    )
    d.set_opacity(S.OP_DATA)
    if point is not None:
        d.move_to(point)
    return d


def data_dot_3d(point=None, **kwargs) -> Dot3D:
    """A 3D data point in the TEAL hero color."""
    d = Dot3D(
        color=kwargs.pop("color", S.DATA),
        radius=kwargs.pop("radius", S.DOT_DATA_3D),
        **kwargs,
    )
    d.set_opacity(S.OP_DATA)
    if point is not None:
        d.move_to(point)
    return d


def hero_arrow(start, end, **kwargs) -> Arrow:
    """The discovered direction. MAGENTA, thicker stroke."""
    return Arrow(
        start=start,
        end=end,
        color=kwargs.pop("color", S.STRUCTURE),
        stroke_width=kwargs.pop("stroke_width", S.STROKE_STRUCTURE),
        buff=kwargs.pop("buff", 0),
        **kwargs,
    )


def hero_arrow_3d(start, end, **kwargs) -> Arrow3D:
    return Arrow3D(
        start=start,
        end=end,
        color=kwargs.pop("color", S.STRUCTURE),
        thickness=kwargs.pop("thickness", 0.03),
        **kwargs,
    )


def residual(start, end, **kwargs) -> DashedLine:
    """Dashed projection / residual line in MUTED."""
    return DashedLine(
        start=start,
        end=end,
        color=kwargs.pop("color", S.SHADOW),
        stroke_width=kwargs.pop("stroke_width", S.STROKE_RESIDUAL),
        dash_length=kwargs.pop("dash_length", 0.12),
        **kwargs,
    )


def BocAxes(**kwargs) -> Axes:
    """2D axes in the house style."""
    axis_config = {"stroke_color": S.FG_DIM, "stroke_width": S.STROKE_AXIS}
    axis_config.update(kwargs.pop("axis_config", {}))
    a = Axes(axis_config=axis_config, **kwargs)
    a.set_opacity(S.OP_AXIS)
    return a


def BocNumberPlane(**kwargs) -> NumberPlane:
    """A grid plane that recedes into the background."""
    background_line_style = {
        "stroke_color": S.GRID,
        "stroke_width": 1,
        "stroke_opacity": S.OP_GRID,
    }
    background_line_style.update(kwargs.pop("background_line_style", {}))
    return NumberPlane(
        background_line_style=background_line_style,
        axis_config={"stroke_color": S.FG_DIM, "stroke_width": S.STROKE_AXIS},
        **kwargs,
    )


def BocThreeDAxes(**kwargs) -> ThreeDAxes:
    axis_config = {"stroke_color": S.FG_DIM, "stroke_width": S.STROKE_AXIS}
    axis_config.update(kwargs.pop("axis_config", {}))
    a = ThreeDAxes(axis_config=axis_config, **kwargs)
    a.set_opacity(S.OP_AXIS)
    return a


# --- Code on screen -----------------------------------------------------------


class _BocCodeStyle(Style):
    """Restrained syntax colors: literals are teal (data you can see),
    everything else is FG / FG_DIM so the magenta highlight bar is the hero."""

    background_color = S.BG_PANEL
    default_style = ""
    styles = {
        Token: S.FG,
        Comment: f"italic {S.FG_DIM}",
        Keyword: S.FG_DIM,
        Operator: S.FG_DIM,
        Punctuation: S.FG_DIM,
        Name: S.FG,
        Name.Builtin: S.FG_DIM,
        String: S.DATA,
        Number: S.DATA,
    }


def code_block(
    source: str,
    language: str = "python",
    highlight: int | Iterable[int] | None = None,
    font_size: float = S.SHORT_CODE_FONT_SIZE,
    line_numbers: bool = False,
) -> Code:
    """A code listing in house colors on a BG_PANEL card.

    `source` is dedented by the caller (use textwrap.dedent). `highlight`
    places the magenta bar on those 1-based lines at construction time, with
    no animation; use highlight_lines() to move it later. The default
    font_size is sized for a 9:16 Short (~27 columns across the safe area);
    pass a smaller one for 16:9 scenes.
    """
    code = Code(
        code=source.strip("\n"),
        language=language,
        style=_BocCodeStyle,
        font=S.FONT_MONO,
        font_size=font_size,
        line_spacing=0.6,
        insert_line_no=line_numbers,
        background="rectangle",
        background_stroke_width=0,
        corner_radius=0.2,
        margin=0.35,
    )
    code.background_mobject.set_fill(S.BG_PANEL, opacity=1).set_stroke(width=0)
    if line_numbers:
        code.line_numbers.set_color(S.MUTED)
    # The bar always exists (invisible until used) and sits above the
    # background, below the text, so animating it never re-layers the group.
    bar = _highlight_bar(code, 1 if highlight is None else highlight)
    if highlight is None:
        bar.set_fill(opacity=0)
    code.highlight_bar = bar
    code.submobjects.insert(1, bar)
    return code


def line_span(lines: int | Iterable[int], n_lines: int) -> tuple[int, int]:
    """(first, last) 1-based line range covered by `lines`. Pure; unit-tested."""
    ls = [lines] if isinstance(lines, int) else list(lines)
    if not ls:
        raise ValueError("highlight needs at least one line")
    lo, hi = min(ls), max(ls)
    if lo < 1 or hi > n_lines:
        raise ValueError(f"lines {lo}..{hi} outside 1..{n_lines}")
    return lo, hi


def _line_centers_y(code: Code) -> list[float]:
    """y of each code line. Blank lines have no glyphs, so fit a uniform pitch
    through the lines that do."""
    rows = code.code.chars
    known = [(i, row.get_center()[1]) for i, row in enumerate(rows) if len(row.submobjects)]
    if len(known) == 1:
        return [known[0][1]] * len(rows)
    (i0, y0), (i1, y1) = known[0], known[-1]
    pitch = (y1 - y0) / (i1 - i0)
    return [y0 + (i - i0) * pitch for i in range(len(rows))]


def _highlight_bar(code: Code, lines: int | Iterable[int]) -> Rectangle:
    ys = _line_centers_y(code)
    lo, hi = line_span(lines, len(ys))
    pitch = abs(ys[1] - ys[0]) if len(ys) > 1 else code.code.height
    top, bottom = ys[lo - 1] + pitch / 2, ys[hi - 1] - pitch / 2
    bg = code.background_mobject
    bar = Rectangle(
        width=bg.width, height=top - bottom,
        fill_color=S.STRUCTURE, fill_opacity=S.OP_GHOST, stroke_width=0,
    )
    return bar.move_to([bg.get_center()[0], (top + bottom) / 2, 0])


def highlight_lines(code: Code, lines: int | Iterable[int]) -> Transform:
    """Animation that puts the translucent magenta bar behind `lines` (1-based).

    First use fades the bar in on those lines; later calls slide/resize it
    (same mobject, so it keeps its identity, ANIMATION_RULES rule 8).
    Only works on a Code built by code_block(). Pass run_time to
    self.play: self.play(highlight_lines(code, 3), run_time=S.BEAT).
    """
    target = _highlight_bar(code, lines)
    bar = code.highlight_bar
    if bar.get_fill_opacity() == 0:  # first use: fade in place, don't slide
        bar.become(target).set_fill(opacity=0)
    return Transform(bar, target)
