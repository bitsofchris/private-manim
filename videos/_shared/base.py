"""Base Scene subclasses with the Bits of Chris defaults baked in."""
from __future__ import annotations

from manim import (
    DOWN,
    UP,
    FadeIn,
    FadeOut,
    Scene,
    Text,
    ThreeDScene,
    config,
)

from videos._shared import style as S


def _caption_text(text: str) -> Text:
    t = Text(text, font=S.FONT, weight="MEDIUM").scale(S.CAPTION_SCALE)
    t.set_color(S.FG)
    return t


class _BocMixin:
    """Shared helpers. Composed into BocScene and Boc3DScene below."""

    def beat(self, kind: str = "BEAT") -> None:
        """Wait one of the three canonical durations: QUICK / BEAT / HOLD."""
        d = {"QUICK": S.QUICK, "BEAT": S.BEAT, "HOLD": S.HOLD}[kind]
        self.wait(d)

    def caption(self, text: str, fixed_in_frame: bool = False) -> Text:
        """Top-center caption. Returns the mobject; you fade it in/out yourself.

        For 3D scenes, pass fixed_in_frame=True so the caption ignores camera
        rotation. Boc3DScene.caption() does this automatically.
        """
        t = _caption_text(text).to_edge(UP)
        if fixed_in_frame:
            self.add_fixed_in_frame_mobjects(t)
            t.set_opacity(0)  # caller fades it in
        return t

    def show_caption(self, text: str, fixed_in_frame: bool = False) -> Text:
        """Caption + fade in. Returns the mobject so you can fade it out later."""
        t = self.caption(text, fixed_in_frame=fixed_in_frame)
        if fixed_in_frame:
            self.play(t.animate.set_opacity(1), run_time=S.QUICK)
        else:
            self.play(FadeIn(t), run_time=S.QUICK)
        return t

    def hide_caption(self, t: Text) -> None:
        self.play(FadeOut(t), run_time=S.QUICK)


class BocScene(_BocMixin, Scene):
    """2D scene with BG_DEEP background and FG default text."""

    def setup(self) -> None:
        config.background_color = S.BG_DEEP
        self.camera.background_color = S.BG_DEEP


class Boc3DScene(_BocMixin, ThreeDScene):
    """3D scene with BG_DEEP background and our default camera orientation."""

    def setup(self) -> None:
        config.background_color = S.BG_DEEP
        self.camera.background_color = S.BG_DEEP
        self.set_camera_orientation(phi=S.CAM_PHI, theta=S.CAM_THETA)

    def caption(self, text: str, fixed_in_frame: bool = True) -> Text:
        # 3D captions default to fixed-in-frame.
        return super().caption(text, fixed_in_frame=fixed_in_frame)

    def show_caption(self, text: str, fixed_in_frame: bool = True) -> Text:
        return super().show_caption(text, fixed_in_frame=fixed_in_frame)
