"""Preconfigured mobjects in the Bits of Chris palette.

Always prefer these over raw Dot/Arrow/Axes so the palette stays consistent.
"""
from __future__ import annotations

from manim import (
    Arrow,
    Arrow3D,
    Axes,
    DashedLine,
    Dot,
    Dot3D,
    NumberPlane,
    ThreeDAxes,
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
