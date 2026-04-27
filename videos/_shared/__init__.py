"""Bits of Chris house style for Manim scenes.

Import order of preference:
    from videos._shared import style as S
    from videos._shared.base import BocScene, Boc3DScene
    from videos._shared.mobjects import data_dot, hero_arrow, residual, BocAxes
"""
from videos._shared import style
from videos._shared.base import BocScene, Boc3DScene
from videos._shared.mobjects import (
    BocAxes,
    BocNumberPlane,
    BocThreeDAxes,
    data_dot,
    data_dot_3d,
    hero_arrow,
    hero_arrow_3d,
    residual,
)

__all__ = [
    "style",
    "BocScene",
    "Boc3DScene",
    "BocAxes",
    "BocNumberPlane",
    "BocThreeDAxes",
    "data_dot",
    "data_dot_3d",
    "hero_arrow",
    "hero_arrow_3d",
    "residual",
]
