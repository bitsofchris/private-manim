"""Preconfigured mobjects in the Bits of Chris palette.

Always prefer these over raw Dot/Arrow/Axes so the palette stays consistent.
"""
from __future__ import annotations

from collections.abc import Iterable

from manim import (
    LEFT,
    PI,
    RIGHT,
    TAU,
    UP,
    Arc,
    ArcBetweenPoints,
    Arrow,
    Arrow3D,
    Axes,
    Code,
    DashedLine,
    Dot,
    Dot3D,
    NumberPlane,
    Rectangle,
    Text,
    ThreeDAxes,
    Transform,
    VGroup,
    VMobject,
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


# --- Token columns and matrices (transformer shorts) -------------------------
# A token is a tall column of cells, one per dimension shown, with a "⋮" row
# standing in for the rest of d. Cell fill opacity encodes |value| so the
# matrix reads at phone size; digits=True also prints the signed value.
# Positive values are DATA teal, negative values SHADOW indigo.


def _cell_style(v: float, color: str | None = None) -> tuple[str, float]:
    mag = min(abs(float(v)), 1.0)
    color = color or (S.DATA if v >= 0 else S.SHADOW)
    return color, S.TOKEN_CELL_OP_MIN + (S.TOKEN_CELL_OP_MAX - S.TOKEN_CELL_OP_MIN) * mag


def _fmt(v: float) -> str:
    return f"{round(float(v), 1) + 0.0:+.1f}"  # + 0.0 turns -0.0 into +0.0


def _cell_text(v: float) -> Text:
    return Text(_fmt(v), font=S.FONT, weight="MEDIUM").scale(S.SHORT_LABEL_SCALE).set_color(S.FG)


class TokenColumn(VGroup):
    """One token's vector: TOKEN_D_SHOWN shaded cells plus a "⋮" row.

    .cells  VGroup of Rectangles (top to bottom)
    .nums   VGroup of Text values (empty unless digits=True)
    .dots   the "⋮" Text
    set_values(new) retargets the colors/opacities (and digits) in place, so
    `self.play(col.animate.set_values(v))` ticks the numbers without swapping
    the mobject (rule 8: a token keeps its identity).
    """

    def __init__(self, values, digits: bool = False, dots: bool = True,
                 color: str | None = None, cell_w: float = S.TOKEN_CELL_W,
                 cell_h: float = S.TOKEN_CELL_H, **kwargs):
        """color=None: teal for +, indigo for -. color=S.STRUCTURE: an update (all
        magenta, opacity by magnitude). dots=False drops the "⋮" row."""
        super().__init__(**kwargs)
        self.values = list(values)[: S.TOKEN_D_SHOWN]
        self.digits = digits
        self.tint = color  # not .color: Mobject owns that attribute
        self.cells, self.nums = VGroup(), VGroup()
        for i, v in enumerate(self.values):
            color, op = _cell_style(v, self.tint)
            cell = Rectangle(width=cell_w, height=cell_h, stroke_color=S.BG_DEEP,
                             stroke_width=S.STROKE_AXIS * 2, fill_color=color, fill_opacity=op)
            cell.move_to([0, -i * cell_h, 0])
            self.cells.add(cell)
            if digits:
                self.nums.add(_cell_text(v).move_to(cell))
        self.dots = VGroup()
        if dots:
            self.dots.add(Text("⋮", font=S.FONT).scale(S.SHORT_LABEL_SCALE).set_color(S.FG_DIM)
                          .move_to([0, -len(self.values) * cell_h, 0]))
        self.add(self.cells, self.nums, self.dots)

    def set_values(self, values) -> "TokenColumn":
        self.values = list(values)[: S.TOKEN_D_SHOWN]
        for cell, v in zip(self.cells, self.values):
            color, op = _cell_style(v, self.tint)
            cell.set_fill(color, opacity=op)
        for num, v in zip(self.nums, self.values):
            num.become(_cell_text(v).move_to(num))
            num.text = _fmt(v)  # become() copies glyphs, not the attribute
        return self


def bracket(top: float, bottom: float, x: float, side, lip: float = S.TOKEN_BRACKET_LIP,
            color: str = S.FG_DIM) -> VMobject:
    """A square bracket from top to bottom at x; side=LEFT opens to the right."""
    dx = -side[0] * lip
    return VMobject(stroke_color=color, stroke_width=S.STROKE_STRUCTURE).set_points_as_corners(
        [[x + dx, top, 0], [x, top, 0], [x, bottom, 0], [x + dx, bottom, 0]])


class TokenMatrix(VGroup):
    """L token columns side by side, optionally under one shared bracket pair.

    values: array-like of shape (L, >= TOKEN_D_SHOWN).
    .columns  VGroup[TokenColumn]   .brackets  VGroup (two VMobjects, maybe empty)
    set_values(new) updates every column in place.
    """

    def __init__(self, values, digits: bool = False, bracketed: bool = True,
                 dots: bool = True, color: str | None = None,
                 col_gap: float = S.TOKEN_COL_GAP, **kwargs):
        super().__init__(**kwargs)
        self.columns = VGroup(*[TokenColumn(row, digits=digits, dots=dots, color=color)
                                for row in values])
        self.columns.arrange(RIGHT, buff=col_gap, aligned_edge=UP)
        self.brackets = VGroup()
        if bracketed:
            top, bottom = self.columns.get_top()[1] + 0.15, self.columns.get_bottom()[1] - 0.15
            self.brackets.add(bracket(top, bottom, self.columns.get_left()[0] - 0.25, LEFT),
                              bracket(top, bottom, self.columns.get_right()[0] + 0.25, RIGHT))
        self.add(self.brackets, self.columns)

    def set_values(self, values) -> "TokenMatrix":
        for col, row in zip(self.columns, values):
            col.set_values(row)
        return self


def attention_arcs(sources, target, weights, color: str = S.STRUCTURE,
                   angle: float = -TAU / 4) -> VGroup:
    """Arcs from the top of each source column into the top of the target.

    Stroke width scales with the weight (ATTN_ARC_MIN..ATTN_ARC_MAX). The
    target's own arc (self-attention) is a small loop above it. Animate with
    Create(arcs, lag_ratio=...) or ShowPassingFlash on a copy.
    """
    arcs = VGroup()
    tgt = target.get_top() + UP * 0.1
    for src, w in zip(sources, weights):
        width = S.ATTN_ARC_MIN + (S.ATTN_ARC_MAX - S.ATTN_ARC_MIN) * float(w)
        start = src.get_top() + UP * 0.1
        if src is target:
            a = Arc(radius=0.45, start_angle=PI, angle=-PI).move_to(tgt + UP * 0.45)
        else:
            ang = angle if start[0] < tgt[0] else -angle
            a = ArcBetweenPoints(start, tgt, angle=ang)
        arcs.add(a.set_stroke(color, width=width))
    return arcs
